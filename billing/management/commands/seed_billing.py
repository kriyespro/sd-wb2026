from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from billing.models import Invoice
from clients.models import ClientAccount
from projects.models import Project


class Command(BaseCommand):
    help = 'Create sample invoices for client accounts'

    def handle(self, *args, **options):
        accounts = list(ClientAccount.objects.all())
        if not accounts:
            self.stdout.write(self.style.WARNING('No client accounts found. Run seed_clients first.'))
            return

        samples = [
            ('WB-INV-1001', 'SEO Retainer — Month 1', Decimal('45000.00'), Invoice.STATUS_SENT),
            ('WB-INV-1002', 'Website Development — Milestone 1', Decimal('125000.00'), Invoice.STATUS_PAID),
            ('WB-INV-1003', 'Meta Ads Management', Decimal('35000.00'), Invoice.STATUS_OVERDUE),
        ]

        for account in accounts:
            project = Project.objects.filter(client_account=account).first()
            for number, title, amount, status in samples:
                Invoice.objects.update_or_create(
                    invoice_number=f'{number}-{account.id}',
                    defaults={
                        'client_account': account,
                        'project': project,
                        'title': title,
                        'amount': amount,
                        'status': status,
                        'due_date': date.today() + timedelta(days=15 if status != Invoice.STATUS_OVERDUE else -5),
                        'notes': 'Sample invoice for demo purposes.',
                    },
                )

        self.stdout.write(self.style.SUCCESS(f'Seeded invoices for {len(accounts)} client account(s).'))
