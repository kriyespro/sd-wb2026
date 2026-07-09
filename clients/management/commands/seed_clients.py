from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from clients.models import ClientAccount, Goal, SupportMessage, SupportTicket
from projects.models import (
    Deliverable,
    Meeting,
    Milestone,
    Project,
    Report,
    ReportMetric,
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed client account with demo projects, reports, and deliverables'

    def handle(self, *args, **options):
        try:
            client_user = User.objects.get(username='client1')
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Run seed_users first (client1 missing).'))
            return

        pm = User.objects.filter(username='pm1').first()

        account, _ = ClientAccount.objects.get_or_create(
            user=client_user,
            defaults={
                'company_name': 'Acme Retail Pvt Ltd',
                'industry': 'E-commerce',
                'account_manager': pm,
            },
        )

        project, _ = Project.objects.get_or_create(
            client_account=account, name='E-commerce SEO & Ads Growth',
            defaults={
                'service_type': 'SEO',
                'description': 'Full-funnel SEO and paid ads to grow organic and paid revenue.',
                'status': Project.STATUS_ACTIVE,
                'progress_percent': 60,
                'project_manager': pm,
                'start_date': date.today() - timedelta(days=60),
            },
        )

        project2, _ = Project.objects.get_or_create(
            client_account=account, name='Website Redesign',
            defaults={
                'service_type': 'Website Development',
                'description': 'Conversion-focused redesign of the main storefront.',
                'status': Project.STATUS_COMPLETED,
                'progress_percent': 100,
                'project_manager': pm,
            },
        )

        if not project.milestones.exists():
            Milestone.objects.bulk_create([
                Milestone(project=project, title='Technical SEO Audit', due_date=date.today() - timedelta(days=45), status=Milestone.STATUS_DONE, order=1),
                Milestone(project=project, title='Keyword Strategy', due_date=date.today() - timedelta(days=30), status=Milestone.STATUS_DONE, order=2),
                Milestone(project=project, title='Content Production', due_date=date.today() + timedelta(days=10), status=Milestone.STATUS_IN_PROGRESS, order=3),
                Milestone(project=project, title='Link Building', due_date=date.today() + timedelta(days=30), status=Milestone.STATUS_PENDING, order=4),
            ])

        # One approved (client-visible) and one pending (hidden) deliverable to demonstrate the rule.
        Deliverable.objects.get_or_create(
            project=project, title='SEO Audit Report (PDF)',
            defaults={
                'description': 'Complete technical audit with prioritized fixes.',
                'file_url': 'https://example.com/audit.pdf',
                'approval_status': Deliverable.APPROVAL_APPROVED,
                'approved_by': pm,
            },
        )
        Deliverable.objects.get_or_create(
            project=project, title='Draft Content Calendar',
            defaults={
                'description': 'Awaiting internal QA before client release.',
                'approval_status': Deliverable.APPROVAL_PENDING,
            },
        )

        report, _ = Report.objects.get_or_create(
            project=project, title='Monthly Performance — Last 30 Days',
            defaults={
                'period': 'Last 30 days',
                'summary': 'Organic traffic and conversions trending up. Paid ROAS stable.',
            },
        )
        if not report.metrics.exists():
            ReportMetric.objects.bulk_create([
                ReportMetric(report=report, label='Organic Traffic', value='24,500', change='+18%'),
                ReportMetric(report=report, label='Conversions', value='412', change='+22%'),
                ReportMetric(report=report, label='Avg. Position', value='6.4', change='+2.1'),
                ReportMetric(report=report, label='Paid ROAS', value='4.2x', change='+0.3x'),
            ])

        Meeting.objects.get_or_create(
            client_account=account, title='Monthly Strategy Review',
            defaults={
                'project': project,
                'scheduled_at': timezone.now() + timedelta(days=5, hours=3),
                'status': Meeting.STATUS_SCHEDULED,
                'notes': 'Review last month performance and plan next sprint.',
            },
        )

        Goal.objects.get_or_create(
            client_account=account, title='Grow organic revenue',
            defaults={'target': '+40% in 6 months', 'progress_percent': 55, 'status': Goal.STATUS_ON_TRACK},
        )
        Goal.objects.get_or_create(
            client_account=account, title='Reduce cost per acquisition',
            defaults={'target': 'Under Rs 350', 'progress_percent': 30, 'status': Goal.STATUS_AT_RISK},
        )

        if not account.tickets.exists():
            ticket = SupportTicket.objects.create(client_account=account, subject='Add tracking to new landing page')
            SupportMessage.objects.create(ticket=ticket, sender=client_user, body='Can you add GA4 tracking to our new promo page?')
            if pm:
                SupportMessage.objects.create(ticket=ticket, sender=pm, body='Sure, we will set it up by tomorrow and confirm.')

        self.stdout.write(self.style.SUCCESS('Client demo data seeded. Login as client1 / client1234'))
