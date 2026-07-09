from django.contrib.auth.models import User
from django.test import TestCase

from billing.models import Invoice
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
