from django.test import Client, TestCase
from django.urls import reverse

from website.models import Lead, JobApplication


class PublicSiteTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get(reverse('website:services'))
        self.assertEqual(response.status_code, 200)

    def test_careers_page_has_job_form(self):
        response = self.client.get(reverse('website:careers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit Job Application')
        self.assertContains(response, 'job-apply-form-container')
        self.assertNotContains(response, 'Apply to Academy →')

    def test_job_apply_creates_application(self):
        response = self.client.post(reverse('website:job_apply'), {
            'name': 'Job Seeker',
            'email': 'job@example.com',
            'phone': '9999999999',
            'role': 'Meta Ads Specialist',
            'application_type': 'fulltime',
            'experience': '2 years',
            'portfolio_url': '',
            'linkedin_url': '',
            'cover_letter': 'I want to join the ads team.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JobApplication.objects.filter(email='job@example.com').exists())
        self.assertContains(response, 'Application received')

    def test_job_apply_blocks_duplicate_email(self):
        JobApplication.objects.create(
            name='Job Seeker', email='dupe@example.com', phone='9999999999',
            role='Meta Ads Specialist', cover_letter='First attempt.',
        )
        response = self.client.post(reverse('website:job_apply'), {
            'name': 'Job Seeker',
            'email': 'dupe@example.com',
            'phone': '8888888888',
            'role': 'SEO Specialist',
            'application_type': 'fulltime',
            'experience': '2 years',
            'portfolio_url': '',
            'linkedin_url': '',
            'cover_letter': 'Second attempt.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JobApplication.objects.filter(email='dupe@example.com').count(), 1)
        self.assertContains(response, "already applied")

    def test_job_apply_blocks_duplicate_phone(self):
        JobApplication.objects.create(
            name='Job Seeker', email='first@example.com', phone='7777777777',
            role='Meta Ads Specialist', cover_letter='First attempt.',
        )
        response = self.client.post(reverse('website:job_apply'), {
            'name': 'Job Seeker',
            'email': 'second@example.com',
            'phone': '7777777777',
            'role': 'SEO Specialist',
            'application_type': 'fulltime',
            'experience': '2 years',
            'portfolio_url': '',
            'linkedin_url': '',
            'cover_letter': 'Second attempt.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JobApplication.objects.filter(phone='7777777777').count(), 1)
        self.assertContains(response, "already applied")

    def test_lead_submit_creates_lead(self):
        response = self.client.post(reverse('website:lead_submit'), {
            'name': 'Test Lead',
            'email': 'lead@example.com',
            'phone': '9999999999',
            'company': 'Test Co',
            'service_interest': 'SEO',
            'message': 'Interested in SEO services',
            'source_page': 'test',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lead.objects.filter(email='lead@example.com').exists())


class PortalAccessTests(TestCase):
    def test_ops_requires_login(self):
        response = self.client.get(reverse('operations:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login/', response.url)

    def test_client_dashboard_requires_login(self):
        response = self.client.get(reverse('clients:dashboard'))
        self.assertEqual(response.status_code, 302)
