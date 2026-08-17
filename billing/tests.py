from unittest.mock import MagicMock, patch

import razorpay
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from billing.models import Invoice
from billing.services import create_razorpay_order, verify_and_mark_paid
from clients.models import ClientAccount
from users.roles import ROLE_CLIENT_OWNER


class BillingTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('client1', 'client@test.com', 'pass1234')
        user.profile.role = ROLE_CLIENT_OWNER
        user.profile.save()
        self.account = ClientAccount.objects.create(user=user, company_name='Test Client')

    def test_invoice_creation(self):
        invoice = Invoice.objects.create(
            client_account=self.account,
            invoice_number='WB-TEST-001',
            title='Test Invoice',
            amount='10000.00',
            due_date='2026-12-31',
        )
        self.assertEqual(str(invoice), 'WB-TEST-001 — Test Client')


class RazorpayServiceTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('client2', 'client2@test.com', 'pass1234')
        user.profile.role = ROLE_CLIENT_OWNER
        user.profile.save()
        self.account = ClientAccount.objects.create(user=user, company_name='Pay Test Co')
        self.invoice = Invoice.objects.create(
            client_account=self.account,
            invoice_number='WB-TEST-002',
            title='Website Sprint',
            amount='15000.00',
            due_date='2026-12-31',
        )

    @patch('billing.services.get_razorpay_client')
    def test_create_razorpay_order_stores_order_id(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.order.create.return_value = {'id': 'order_TEST123', 'amount': 1500000}
        mock_get_client.return_value = mock_client

        order = create_razorpay_order(self.invoice)

        self.assertEqual(order['id'], 'order_TEST123')
        mock_client.order.create.assert_called_once_with({
            'amount': 1500000,
            'currency': 'INR',
            'receipt': 'WB-TEST-002',
            'notes': {'invoice_id': str(self.invoice.pk)},
        })
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.razorpay_order_id, 'order_TEST123')

    def test_create_razorpay_order_rejects_already_paid_invoice(self):
        self.invoice.status = Invoice.STATUS_PAID
        self.invoice.save()
        with self.assertRaises(ValueError):
            create_razorpay_order(self.invoice)

    @patch('billing.services.get_razorpay_client')
    def test_verify_and_mark_paid_success(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        self.invoice.razorpay_order_id = 'order_TEST123'
        self.invoice.save()

        verify_and_mark_paid(self.invoice, 'order_TEST123', 'pay_TEST123', 'sig_TEST123')

        mock_client.utility.verify_payment_signature.assert_called_once_with({
            'razorpay_order_id': 'order_TEST123',
            'razorpay_payment_id': 'pay_TEST123',
            'razorpay_signature': 'sig_TEST123',
        })
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.STATUS_PAID)
        self.assertEqual(self.invoice.razorpay_payment_id, 'pay_TEST123')
        self.assertIsNotNone(self.invoice.paid_at)

    def test_verify_rejects_order_id_mismatch(self):
        self.invoice.razorpay_order_id = 'order_REAL'
        self.invoice.save()
        with self.assertRaises(ValueError):
            verify_and_mark_paid(self.invoice, 'order_FAKE', 'pay_x', 'sig_x')
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.STATUS_SENT)

    @patch('billing.services.get_razorpay_client')
    def test_verify_propagates_bad_signature(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.utility.verify_payment_signature.side_effect = razorpay.errors.SignatureVerificationError('bad sig')
        mock_get_client.return_value = mock_client
        self.invoice.razorpay_order_id = 'order_TEST123'
        self.invoice.save()

        with self.assertRaises(razorpay.errors.SignatureVerificationError):
            verify_and_mark_paid(self.invoice, 'order_TEST123', 'pay_TEST123', 'bad_sig')
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.STATUS_SENT)


class InvoicePaymentViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('client3', 'client3@test.com', 'pass1234')
        self.owner.profile.role = ROLE_CLIENT_OWNER
        self.owner.profile.save()
        self.account = ClientAccount.objects.create(user=self.owner, company_name='Owner Co')
        self.invoice = Invoice.objects.create(
            client_account=self.account,
            invoice_number='WB-TEST-003',
            title='SEO Retainer',
            amount='8000.00',
            due_date='2026-12-31',
        )

        self.other = User.objects.create_user('client4', 'client4@test.com', 'pass1234')
        self.other.profile.role = ROLE_CLIENT_OWNER
        self.other.profile.save()
        ClientAccount.objects.create(user=self.other, company_name='Other Co')

    @patch('clients.views.create_razorpay_order')
    def test_pay_view_scoped_to_own_invoice(self, mock_create_order):
        mock_create_order.return_value = {'id': 'order_ABC', 'amount': 800000}
        self.client.login(username='client3', password='pass1234')
        url = reverse('clients:invoice_pay', kwargs={'pk': self.invoice.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'order_ABC')

    def test_other_client_cannot_pay_someone_elses_invoice(self):
        self.client.login(username='client4', password='pass1234')
        url = reverse('clients:invoice_pay', kwargs={'pk': self.invoice.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('website:home'))

    @patch('clients.views.verify_and_mark_paid')
    def test_verify_view_scoped_to_own_invoice(self, mock_verify):
        self.client.login(username='client3', password='pass1234')
        url = reverse('clients:invoice_verify', kwargs={'pk': self.invoice.pk})
        response = self.client.post(url, {
            'razorpay_order_id': 'order_ABC',
            'razorpay_payment_id': 'pay_ABC',
            'razorpay_signature': 'sig_ABC',
        })
        self.assertEqual(response.status_code, 302)
        mock_verify.assert_called_once()

    def test_other_client_cannot_verify_someone_elses_invoice(self):
        self.client.login(username='client4', password='pass1234')
        url = reverse('clients:invoice_verify', kwargs={'pk': self.invoice.pk})
        response = self.client.post(url, {
            'razorpay_order_id': 'order_ABC',
            'razorpay_payment_id': 'pay_ABC',
            'razorpay_signature': 'sig_ABC',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('website:home'))
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.STATUS_SENT)
