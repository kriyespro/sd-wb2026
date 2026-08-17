from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from billing.models import Invoice
from projects.models import Deliverable, Meeting, Milestone, Project, Report, ReportMetric

from .models import ClientAccount, SupportMessage, SupportTicket
from .services import get_client_attention_items


class ClientPortalListPaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('client1', 'client1@test.com', 'pass1234')
        self.user.profile.role = 'client_owner'
        self.user.profile.save()
        self.account = ClientAccount.objects.create(user=self.user, company_name='Acme Co')
        self.project = Project.objects.create(client_account=self.account, name='Acme Project')
        self.client.login(username='client1', password='pass1234')

    def test_files_view_paginates(self):
        for i in range(25):
            Deliverable.objects.create(
                project=self.project, title=f'File {i}', approval_status='approved',
            )
        response = self.client.get(reverse('clients:files'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'File '), 20)
        self.assertContains(response, 'Next')
        self.assertNotContains(response, 'Previous')

        response = self.client.get(reverse('clients:files') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'File '), 5)
        self.assertContains(response, 'Previous')

    def test_meetings_view_paginates(self):
        for i in range(22):
            Meeting.objects.create(
                client_account=self.account, title=f'Meeting {i}',
                scheduled_at='2026-08-01T10:00:00Z',
            )
        response = self.client.get(reverse('clients:meetings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'Meeting '), 20)

    def test_invoices_view_paginates(self):
        for i in range(21):
            Invoice.objects.create(
                client_account=self.account, invoice_number=f'INV-{i}',
                title='Retainer', due_date=date(2026, 8, 1),
            )
        response = self.client.get(reverse('clients:invoices'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'INV-'), 20)

    def test_support_view_paginates(self):
        for i in range(21):
            SupportTicket.objects.create(client_account=self.account, subject=f'Ticket {i}')
        response = self.client.get(reverse('clients:support'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'Ticket '), 20)

    def test_analytics_view_caps_metrics_at_eight(self):
        for r in range(3):
            report = Report.objects.create(project=self.project, title=f'Report {r}')
            for m in range(4):
                ReportMetric.objects.create(report=report, label=f'M{r}-{m}', value='10')
        response = self.client.get(reverse('clients:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.count(b'M0-') + response.content.count(b'M1-') + response.content.count(b'M2-'), 8)

    def test_roi_view_counts(self):
        Project.objects.create(
            client_account=self.account, name='Done', status=Project.STATUS_COMPLETED,
        )
        response = self.client.get(reverse('clients:roi'))
        self.assertEqual(response.status_code, 200)


class ClientAttentionItemsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('client2', 'client2@test.com', 'pass1234')
        self.user.profile.role = 'client_owner'
        self.user.profile.save()
        self.account = ClientAccount.objects.create(user=self.user, company_name='Beta Co')
        self.project = Project.objects.create(client_account=self.account, name='Beta Project')
        self.client.login(username='client2', password='pass1234')

    def test_all_clear_when_nothing_needs_attention(self):
        self.assertEqual(get_client_attention_items(self.account), [])
        response = self.client.get(reverse('clients:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All clear')

    def test_all_clear_for_no_account(self):
        self.assertEqual(get_client_attention_items(None), [])

    def test_surfaces_overdue_invoice_milestone_meeting_and_ticket_reply(self):
        Invoice.objects.create(
            client_account=self.account, invoice_number='INV-OD1', title='Retainer',
            due_date=date(2026, 1, 1), status=Invoice.STATUS_OVERDUE,
        )
        Milestone.objects.create(
            project=self.project, title='Kickoff', due_date=date(2026, 1, 1),
            status=Milestone.STATUS_PENDING,
        )
        Meeting.objects.create(
            client_account=self.account, title='Check-in',
            scheduled_at=timezone.now() + timedelta(days=2),
            status=Meeting.STATUS_SCHEDULED,
        )
        staff = User.objects.create_user('staffreply', 'staffreply@test.com', 'pass1234')
        ticket = SupportTicket.objects.create(client_account=self.account, subject='Question')
        SupportMessage.objects.create(ticket=ticket, sender=staff, body='We are looking into it')

        items = get_client_attention_items(self.account)
        tones_by_href = {item['href_name']: item['tone'] for item in items}
        self.assertEqual(tones_by_href['clients:invoices'], 'rose')
        self.assertEqual(tones_by_href['clients:projects'], 'orange')
        self.assertEqual(tones_by_href['clients:meetings'], 'brand')
        self.assertEqual(tones_by_href['clients:support'], 'teal')

        response = self.client.get(reverse('clients:dashboard'))
        self.assertContains(response, 'Needs your attention')
        self.assertContains(response, 'overdue invoice')

    def test_ticket_not_flagged_when_client_sent_last_message(self):
        ticket = SupportTicket.objects.create(client_account=self.account, subject='Question')
        SupportMessage.objects.create(ticket=ticket, sender=self.user, body='Any update?')
        items = get_client_attention_items(self.account)
        self.assertFalse(any(item['href_name'] == 'clients:support' for item in items))
