from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.roles import ROLE_SALES, ROLE_SUPER_ADMIN
from partners.models import PartnerLead, PartnerProfile
from website.models import JobApplication, Lead


class LeadPipelineTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@test.com', 'pass1234')
        self.admin.is_superuser = True
        self.admin.save()
        self.admin.profile.role = ROLE_SUPER_ADMIN
        self.admin.profile.save()
        self.sales = User.objects.create_user('sales1', 'sales@test.com', 'pass1234')
        self.sales.profile.role = ROLE_SALES
        self.sales.profile.save()
        self.lead = Lead.objects.create(
            name='Pipeline Lead',
            email='pipeline@example.com',
            company='Acme',
            service_interest='SEO',
        )
        self.client.login(username='admin', password='pass1234')

    def test_lead_status_update(self):
        url = reverse('operations:lead_status', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'status': Lead.STATUS_QUALIFIED})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, Lead.STATUS_QUALIFIED)

    def test_lead_assign(self):
        url = reverse('operations:lead_assign', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'assigned_to': self.sales.pk})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.assigned_to_id, self.sales.pk)

    def test_lead_convert(self):
        url = reverse('operations:lead_convert', kwargs={'pk': self.lead.pk})
        response = self.client.post(url, {'project_name': 'Acme SEO Project'})
        self.assertEqual(response.status_code, 200)
        self.lead.refresh_from_db()
        self.assertTrue(self.lead.is_converted)
        self.assertEqual(self.lead.status, Lead.STATUS_WON)

    def test_mission_control_live_partial(self):
        response = self.client.get(reverse('operations:live_mission'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ops-stats-bar', response.content)
        self.assertIn(b'Pipeline Lead', response.content)

    def test_leads_live_partial(self):
        response = self.client.get(reverse('operations:live_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lead-', response.content)
        self.assertIn(b'Pipeline Lead', response.content)

    def test_job_applications_superuser_table(self):
        JobApplication.objects.create(
            name='Applicant One',
            email='applicant@example.com',
            phone='9999999999',
            role='Meta Ads Specialist',
            cover_letter='I want this role.',
        )
        response = self.client.get(reverse('operations:job_applications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Applicant One')
        self.assertContains(response, 'Meta Ads Specialist')
        self.assertContains(response, '<table')

    def test_job_applications_sales_forbidden(self):
        self.client.login(username='sales1', password='pass1234')
        response = self.client.get(reverse('operations:job_applications'))
        self.assertEqual(response.status_code, 302)

    def test_dgc_leads_superuser_table(self):
        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcops', 'dgcops@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCOPS1')
        PartnerLead.objects.create(
            partner=partner,
            name='Ops Visible Lead',
            phone='9000000001',
            company='Visible Mills',
            interest='D2C',
        )
        response = self.client.get(reverse('operations:dgc_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ops Visible Lead')
        self.assertContains(response, 'DGCOPS1')
        self.assertContains(response, '<table')

    def test_dgc_leads_sales_forbidden(self):
        self.client.login(username='sales1', password='pass1234')
        response = self.client.get(reverse('operations:dgc_leads'))
        self.assertEqual(response.status_code, 302)

    def test_dgc_lead_status_won_creates_commission(self):
        from decimal import Decimal

        from users.roles import ROLE_PARTNER

        partner_user = User.objects.create_user('dgcops2', 'dgcops2@test.com', 'pass1234')
        partner_user.profile.role = ROLE_PARTNER
        partner_user.profile.save()
        partner = PartnerProfile.objects.create(user=partner_user, code='DGCOPS2')
        lead = PartnerLead.objects.create(
            partner=partner,
            name='Won Via Ops',
            phone='9000000002',
            deal_value=Decimal('10000.00'),
            status=PartnerLead.STATUS_NEW,
        )
        url = reverse('operations:dgc_lead_status', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'status': PartnerLead.STATUS_WON})
        self.assertEqual(response.status_code, 200)
        lead.refresh_from_db()
        self.assertEqual(lead.status, PartnerLead.STATUS_WON)
        self.assertTrue(lead.commissions.exists())
        self.assertEqual(lead.commissions.first().amount, Decimal('2000.00'))
