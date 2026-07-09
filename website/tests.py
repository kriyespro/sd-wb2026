from django.test import Client, TestCase
from django.urls import reverse

from website.models import Lead


class PublicSiteTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get(reverse('website:services'))
        self.assertEqual(response.status_code, 200)

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
