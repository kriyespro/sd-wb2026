from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from partners.models import (
    Commission,
    DgcApplication,
    PartnerLead,
    PartnerProfile,
    ResellerOffer,
)
from partners.services import (
    approve_dgc_application,
    can_request_payout,
    cancel_dgc_application,
    create_payout_request,
    pause_dgc_application,
    place_order,
    resume_dgc_application,
    update_lead_status,
)
from users.roles import ROLE_PARTNER, ROLE_SALES, ROLE_SUPER_ADMIN


class DgcPartnerTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@test.com', 'pass1234')
        self.admin.is_superuser = True
        self.admin.save()
        self.admin.profile.role = ROLE_SUPER_ADMIN
        self.admin.profile.save()

        self.offer = ResellerOffer.objects.create(
            title='Test Package',
            price=Decimal('10000.00'),
            commission_percent=Decimal('20.00'),
            is_active=True,
        )

    def test_public_apply(self):
        response = self.client.post(reverse('partners_public:apply'), {
            'name': 'Rita Partner',
            'email': 'rita@example.com',
            'phone': '9999999999',
            'city': 'Surat',
            'experience': '3 years marketing',
            'why': 'I want to sell D2C packages.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DgcApplication.objects.filter(email='rita@example.com').exists())

    def test_approve_creates_partner_portal(self):
        app = DgcApplication.objects.create(
            name='Rita Partner',
            email='rita2@example.com',
            phone='9999999998',
            why='Grow with WB',
        )
        user, password = approve_dgc_application(app, self.admin)
        self.assertEqual(user.profile.role, ROLE_PARTNER)
        self.assertTrue(hasattr(user, 'partner_profile'))
        app.refresh_from_db()
        self.assertEqual(app.temp_password, password)
        self.assertEqual(app.partner_user_id, user.id)
        self.client.login(username=user.username, password=password)
        # Temp password → must change password before the portal unlocks.
        response = self.client.get(reverse('partners:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:force_password_change'))

        response = self.client.post(reverse('users:force_password_change'), {
            'old_password': password,
            'new_password1': 'BrandNewPass123!',
            'new_password2': 'BrandNewPass123!',
        })
        self.assertEqual(response.status_code, 302)
        user.partner_profile.refresh_from_db()
        self.assertFalse(user.partner_profile.must_change_password)
        app.refresh_from_db()
        self.assertEqual(app.temp_password, '')

        response = self.client.get(reverse('partners:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_pause_resume_cancel_partner_access(self):
        app = DgcApplication.objects.create(
            name='Pause Partner',
            email='pause@example.com',
            phone='9999999997',
            why='Test pause flow',
        )
        user, _password = approve_dgc_application(app, self.admin)
        pause_dgc_application(app, self.admin)
        app.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(app.status, DgcApplication.STATUS_PAUSED)
        self.assertFalse(user.is_active)
        self.assertFalse(user.partner_profile.is_active)

        resume_dgc_application(app, self.admin)
        app.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(app.status, DgcApplication.STATUS_APPROVED)
        self.assertTrue(user.is_active)
        self.assertTrue(user.partner_profile.is_active)

        cancel_dgc_application(app, self.admin)
        app.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(app.status, DgcApplication.STATUS_CANCELLED)
        self.assertFalse(user.is_active)
        self.assertFalse(user.partner_profile.is_active)
        with self.assertRaises(ValueError):
            resume_dgc_application(app, self.admin)

    def test_order_creates_commission(self):
        user = User.objects.create_user('dgcx', 'dgcx@test.com', 'pass1234')
        user.profile.role = ROLE_PARTNER
        user.profile.save()
        partner = PartnerProfile.objects.create(user=user, code='DGC9999')
        order = place_order(partner, self.offer, quantity=2)
        self.assertEqual(order.total, Decimal('20000.00'))
        commission = Commission.objects.get(order=order)
        self.assertEqual(commission.amount, Decimal('4000.00'))

    def test_won_lead_creates_commission(self):
        user = User.objects.create_user('dgcy', 'dgcy@test.com', 'pass1234')
        user.profile.role = ROLE_PARTNER
        user.profile.save()
        partner = PartnerProfile.objects.create(user=user, code='DGC8888')
        lead = PartnerLead.objects.create(
            partner=partner,
            name='Factory Lead',
            phone='8888888888',
            deal_value=Decimal('50000.00'),
        )
        update_lead_status(lead, PartnerLead.STATUS_WON)
        self.assertTrue(Commission.objects.filter(lead=lead).exists())

    def test_payout_only_on_21st(self):
        user = User.objects.create_user('dgcz', 'dgcz@test.com', 'pass1234')
        user.profile.role = ROLE_PARTNER
        user.profile.save()
        partner = PartnerProfile.objects.create(user=user, code='DGC7777')
        place_order(partner, self.offer, quantity=1)

        with patch('partners.services.timezone.localdate', return_value=date(2026, 7, 10)):
            self.assertFalse(can_request_payout())
            with self.assertRaises(ValueError):
                create_payout_request(partner, today=date(2026, 7, 10))

        with patch('partners.services.timezone.localdate', return_value=date(2026, 7, 21)):
            self.assertTrue(can_request_payout(date(2026, 7, 21)))
            payout = create_payout_request(partner, today=date(2026, 7, 21))
            self.assertEqual(payout.amount, Decimal('2000.00'))
            self.assertTrue(
                Commission.objects.filter(
                    partner=partner, status=Commission.STATUS_REQUESTED,
                ).exists(),
            )

    def test_orders_view_paginates(self):
        user = User.objects.create_user('dgcpage', 'dgcpage@test.com', 'pass1234')
        user.profile.role = ROLE_PARTNER
        user.profile.save()
        partner = PartnerProfile.objects.create(user=user, code='DGCPAGE1')
        for _ in range(22):
            place_order(partner, self.offer, quantity=1)
        self.client.login(username='dgcpage', password='pass1234')
        response = self.client.get(reverse('partners:orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Next')
        response = self.client.get(reverse('partners:orders') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Previous')

    def test_partner_can_submit_lead(self):
        user = User.objects.create_user('dgclead', 'dgclead@test.com', 'pass1234')
        user.profile.role = ROLE_PARTNER
        user.profile.save()
        PartnerProfile.objects.create(user=user, code='DGCLEAD1')
        self.client.login(username='dgclead', password='pass1234')
        response = self.client.post(reverse('partners:lead_create'), {
            'name': 'Surat Mill',
            'phone': '9876501234',
            'email': 'mill@example.com',
            'company': 'Surat Mill Pvt',
            'interest': 'Meta Ads',
            'notes': 'Ready to go D2C',
            'deal_value': '40000',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PartnerLead.objects.filter(name='Surat Mill', partner__code='DGCLEAD1').exists())

    def test_google_partner_kyc_then_admin_approve(self):
        from partners.services import submit_partner_kyc
        from users.services import provision_public_signup

        user = User.objects.create_user('googledgc', 'googledgc@gmail.com', 'pass1234')
        user.first_name = 'Google'
        user.last_name = 'Partner'
        user.save()
        provision_public_signup(user, ROLE_PARTNER)
        self.assertFalse(user.partner_profile.is_active)

        self.client.login(username='googledgc', password='pass1234')
        r = self.client.get(reverse('partners:offers'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('partners:profile'))

        app = submit_partner_kyc(user, {
            'name': 'Google Partner',
            'email': 'googledgc@gmail.com',
            'phone': '9876543210',
            'city': 'Surat',
            'address': 'Ring Road, Surat 395002',
            'experience': '5 years sales',
            'why': 'Want to resell ecommerce packages',
            'pan_number': 'ABCDE1234F',
            'aadhaar_last4': '4321',
            'upi_id': 'google@upi',
            'bank_account': '1234567890',
            'bank_ifsc': 'HDFC0001234',
        })
        self.assertEqual(app.status, DgcApplication.STATUS_NEW)
        self.assertEqual(app.partner_user_id, user.id)
        self.assertEqual(app.pan_number, 'ABCDE1234F')

        approved_user, temp = approve_dgc_application(app, self.admin)
        self.assertEqual(approved_user.id, user.id)
        self.assertEqual(temp, '')
        user.partner_profile.refresh_from_db()
        self.assertTrue(user.partner_profile.is_active)
        self.assertEqual(user.partner_profile.upi_id, 'google@upi')

        r = self.client.get(reverse('partners:offers'))
        self.assertEqual(r.status_code, 200)

    def test_kyc_form_post(self):
        from users.services import provision_public_signup

        user = User.objects.create_user('kycdgc', 'kycdgc@gmail.com', 'pass1234')
        provision_public_signup(user, ROLE_PARTNER)
        self.client.login(username='kycdgc', password='pass1234')
        r = self.client.post(reverse('partners:profile'), {
            'name': 'KYC Person',
            'email': 'kycdgc@gmail.com',
            'phone': '9000000001',
            'city': 'Ahmedabad',
            'address': 'SG Highway',
            'experience': '2 years',
            'why': 'Join DGC network',
            'pan_number': 'ABCDE1234F',
            'aadhaar_last4': '9999',
            'upi_id': '',
            'bank_account': '',
            'bank_ifsc': '',
        })
        self.assertEqual(r.status_code, 302)
        app = DgcApplication.objects.get(partner_user=user)
        self.assertEqual(app.city, 'Ahmedabad')
        self.assertEqual(app.status, DgcApplication.STATUS_NEW)
