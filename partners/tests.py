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
