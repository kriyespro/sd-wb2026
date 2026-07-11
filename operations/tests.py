from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.roles import ROLE_SALES, ROLE_SUPER_ADMIN
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
