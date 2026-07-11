"""Seed realistic Indian textile / D2C demo data for Mission Control (/ops/)."""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from academy.models import AdmissionApplication
from billing.models import Invoice
from clients.models import ClientAccount
from partners.models import (
    Commission,
    DgcApplication,
    PartnerLead,
    PartnerProfile,
    PayoutRequest,
)
from projects.models import Deliverable, Project
from website.models import JobApplication, Lead

User = get_user_model()


def _backdate(model, pk, days=0, hours=0, touch_updated=True):
    """Override auto_now_add timestamps for a lived-in demo feel."""
    when = timezone.now() - timedelta(days=days, hours=hours)
    model.objects.filter(pk=pk).update(created_at=when)
    if touch_updated and hasattr(model, 'updated_at'):
        model.objects.filter(pk=pk).update(updated_at=when)


class Command(BaseCommand):
    help = 'Seed Indian textile/D2C demo data for Mission Control (/ops/)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush-demo',
            action='store_true',
            help='Remove previous demo-tagged rows before seeding (emails ending @demo.wb.in)',
        )

    def handle(self, *args, **options):
        if options['flush_demo']:
            self._flush_demo()

        sales = User.objects.filter(username='sales1').first()
        pm = User.objects.filter(username='pm1').first()
        partner = PartnerProfile.objects.filter(user__username='dgc1').first()
        if not partner:
            self.stdout.write(self.style.WARNING('No dgc1 partner — run seed_partners first for DGC leads.'))

        self._seed_inbound_leads(sales)
        self._seed_job_applications()
        self._seed_academy()
        self._seed_dgc_applications()
        if partner:
            self._seed_dgc_leads(partner)
            self._seed_payout(partner)
        self._seed_clients_projects_billing(pm)
        self._seed_qa_deliverables(pm)

        self.stdout.write(self.style.SUCCESS(
            'Ops demo data ready. Login admin / admin1234 → /ops/\n'
            'Re-run safe anytime. To reset demo rows: python manage.py seed_ops_demo --flush-demo'
        ))

    def _flush_demo(self):
        Lead.objects.filter(email__endswith='@demo.wb.in').delete()
        JobApplication.objects.filter(email__endswith='@demo.wb.in').delete()
        AdmissionApplication.objects.filter(email__endswith='@demo.wb.in').delete()
        DgcApplication.objects.filter(email__endswith='@demo.wb.in').delete()
        PartnerLead.objects.filter(email__endswith='@demo.wb.in').delete()
        Invoice.objects.filter(invoice_number__startswith='WB-DEMO-').delete()
        Project.objects.filter(name__startswith='[Demo]').delete()
        ClientAccount.objects.filter(company_name__startswith='[Demo]').delete()
        self.stdout.write('Flushed previous @demo.wb.in / WB-DEMO rows.')

    def _seed_inbound_leads(self, sales):
        rows = [
            # New / unassigned — action needed
            {
                'name': 'Ramesh Patel',
                'email': 'ramesh.patel@demo.wb.in',
                'phone': '9876512340',
                'company': 'Shree Ambika Sarees',
                'service_interest': 'Meta Ads + Prepaid Store',
                'message': 'Wholesale margins are stuck at 8–10%. Want daily prepaid orders from pan-India buyers.',
                'source_page': '/contact/',
                'status': Lead.STATUS_NEW,
                'assigned_to': None,
                'days': 0, 'hours': 4,
            },
            {
                'name': 'Priya Agarwal',
                'email': 'priya.agarwal@demo.wb.in',
                'phone': '9825011122',
                'company': 'Tirupur Knit Factory',
                'service_interest': 'eCommerce + WhatsApp Automation',
                'message': 'Making 2,000 tees/day for traders. Ready to sell direct under our own brand.',
                'source_page': '/services/',
                'status': Lead.STATUS_NEW,
                'assigned_to': None,
                'days': 1, 'hours': 2,
            },
            {
                'name': 'Amit Shah',
                'email': 'amit.shah@demo.wb.in',
                'phone': '9904412345',
                'company': 'Rangoli Kurtis, Surat',
                'service_interest': 'Google Shopping Ads',
                'message': 'High-SKU ethnic catalog. Need shopping ads + prepaid checkout.',
                'source_page': '/pricing/',
                'status': Lead.STATUS_NEW,
                'assigned_to': sales,
                'days': 0, 'hours': 10,
            },
            # Contacted / qualified / proposal
            {
                'name': 'Neha Desai',
                'email': 'neha.desai@demo.wb.in',
                'phone': '9687612345',
                'company': 'Loom & Loom Denim',
                'service_interest': 'Full Growth Plan',
                'message': 'Jeans factory in Ahmedabad. Exploring ₹35k Growth package.',
                'source_page': '/startup/',
                'status': Lead.STATUS_CONTACTED,
                'assigned_to': sales,
                'days': 3, 'hours': 0,
            },
            {
                'name': 'Vikram Mehta',
                'email': 'vikram.mehta@demo.wb.in',
                'phone': '9376210987',
                'company': 'Banarasi Weaves Co.',
                'service_interest': 'Brand Identity + Store',
                'message': 'Premium saree brand. Want brand kit + Shopify-style store.',
                'source_page': '/case-studies/',
                'status': Lead.STATUS_QUALIFIED,
                'assigned_to': sales,
                'days': 5, 'hours': 0,
            },
            {
                'name': 'Sunita Jain',
                'email': 'sunita.jain@demo.wb.in',
                'phone': '9426511223',
                'company': 'Jain Dupatta House',
                'service_interest': 'SEO + Content',
                'message': 'Want organic traffic for festive collections.',
                'source_page': '/services/seo/',
                'status': Lead.STATUS_PROPOSAL,
                'assigned_to': sales,
                'days': 8, 'hours': 0,
            },
            # Won / lost
            {
                'name': 'Karan Bansal',
                'email': 'karan.bansal@demo.wb.in',
                'phone': '9810012345',
                'company': 'Urban Ethnic Pvt Ltd',
                'service_interest': 'Scale Package',
                'message': 'Signed Growth plan — store + Meta + Google.',
                'source_page': '/contact/',
                'status': Lead.STATUS_WON,
                'assigned_to': sales,
                'days': 20, 'hours': 0,
            },
            {
                'name': 'Farhan Qureshi',
                'email': 'farhan.q@demo.wb.in',
                'phone': '9898011122',
                'company': 'Qureshi Embroidery Works',
                'service_interest': 'Meta Ads',
                'message': 'Budget too low for retainer right now.',
                'source_page': '/pricing/',
                'status': Lead.STATUS_LOST,
                'assigned_to': sales,
                'days': 14, 'hours': 0,
            },
        ]
        for row in rows:
            days, hours = row.pop('days'), row.pop('hours')
            lead, created = Lead.objects.update_or_create(
                email=row['email'],
                defaults=row,
            )
            # Keep won leads' updated_at recent so "won this month" KPI lights up
            _backdate(
                Lead, lead.pk, days=days, hours=hours,
                touch_updated=(row['status'] != Lead.STATUS_WON),
            )
            if row['status'] == Lead.STATUS_WON:
                Lead.objects.filter(pk=lead.pk).update(updated_at=timezone.now())
            self.stdout.write(f"  Lead {'+' if created else '~'} {lead.name} ({lead.status})")

    def _seed_job_applications(self):
        rows = [
            {
                'name': 'Ananya Sharma',
                'email': 'ananya.sharma@demo.wb.in',
                'phone': '9876500111',
                'role': 'Meta Ads Specialist',
                'application_type': JobApplication.TYPE_FULLTIME,
                'experience': '2.5 years — fashion D2C brands',
                'cover_letter': 'Ran Meta ads for kurti and saree brands in Surat. Comfortable with creative testing and ROAS reporting.',
                'status': JobApplication.STATUS_NEW,
                'days': 1,
            },
            {
                'name': 'Rohit Verma',
                'email': 'rohit.verma@demo.wb.in',
                'phone': '9811122233',
                'role': 'Frontend AI Designer',
                'application_type': JobApplication.TYPE_FULLTIME,
                'experience': '3 years — Figma + Tailwind',
                'cover_letter': 'Built catalog UIs for high-SKU fashion stores. Interested in AI-assisted design workflows.',
                'status': JobApplication.STATUS_REVIEW,
                'days': 4,
            },
            {
                'name': 'Pooja Nair',
                'email': 'pooja.nair@demo.wb.in',
                'phone': '9845012345',
                'role': 'Backoffice Executive',
                'application_type': JobApplication.TYPE_FULLTIME,
                'experience': '1.5 years — order ops',
                'cover_letter': 'Handled prepaid order desks and WhatsApp follow-ups for a Tirupur garment unit.',
                'status': JobApplication.STATUS_INTERVIEW,
                'days': 6,
            },
            {
                'name': 'Siddharth Iyer',
                'email': 'sid.iyer@demo.wb.in',
                'phone': '9884011122',
                'role': 'Graphic Designer',
                'application_type': JobApplication.TYPE_INTERNSHIP,
                'experience': 'Fresher — NID portfolio',
                'cover_letter': 'Looking for internship designing product creatives for textile D2C ads.',
                'status': JobApplication.STATUS_NEW,
                'days': 0,
            },
            {
                'name': 'Meera Joshi',
                'email': 'meera.joshi@demo.wb.in',
                'phone': '9822099887',
                'role': 'Marketing Executive',
                'application_type': JobApplication.TYPE_FULLTIME,
                'experience': '4 years — digital marketing',
                'cover_letter': 'Led campaigns for ethnic wear brands. Strong on WhatsApp commerce and weekly reporting.',
                'status': JobApplication.STATUS_REVIEW,
                'days': 3,
            },
        ]
        for row in rows:
            days = row.pop('days')
            app, created = JobApplication.objects.update_or_create(
                email=row['email'],
                defaults=row,
            )
            _backdate(JobApplication, app.pk, days=days)
            self.stdout.write(f"  Job {'+' if created else '~'} {app.name} — {app.role}")

    def _seed_academy(self):
        rows = [
            {
                'name': 'Aarav Kapoor',
                'email': 'aarav.kapoor@demo.wb.in',
                'phone': '9876001122',
                'education': 'BBA — Symbiosis, Pune',
                'course_interest': 'Digital Marketing Specialist Track',
                'motivation': 'Want hands-on Meta + Google training on real Surat client projects.',
                'status': AdmissionApplication.STATUS_NEW,
                'days': 1,
            },
            {
                'name': 'Isha Reddy',
                'email': 'isha.reddy@demo.wb.in',
                'phone': '9000012345',
                'education': 'B.Tech CSE — VIT',
                'course_interest': 'SEO Specialist Track',
                'motivation': 'Career switch into SEO for fashion eCommerce catalogs.',
                'status': AdmissionApplication.STATUS_NEW,
                'days': 2,
            },
            {
                'name': 'Yash Thakkar',
                'email': 'yash.thakkar@demo.wb.in',
                'phone': '9725011122',
                'education': 'Diploma — Fashion Merchandising, NIFT',
                'course_interest': 'AI & Automation for Growth',
                'motivation': 'From a weaving family in Surat — want to run F2C systems for our unit.',
                'status': AdmissionApplication.STATUS_REVIEW,
                'days': 5,
            },
            {
                'name': 'Fatima Khan',
                'email': 'fatima.khan@demo.wb.in',
                'phone': '9819012345',
                'education': 'BA Mass Comm — Mumbai University',
                'course_interest': 'Content & Social for D2C',
                'motivation': 'Create product stories for saree and kurti brands.',
                'status': AdmissionApplication.STATUS_NEW,
                'days': 0,
            },
        ]
        for row in rows:
            days = row.pop('days')
            app, created = AdmissionApplication.objects.update_or_create(
                email=row['email'],
                defaults=row,
            )
            _backdate(AdmissionApplication, app.pk, days=days)
            self.stdout.write(f"  Academy {'+' if created else '~'} {app.name}")

    def _seed_dgc_applications(self):
        rows = [
            {
                'name': 'Hardik Solanki',
                'email': 'hardik.solanki@demo.wb.in',
                'phone': '9825112233',
                'city': 'Surat',
                'experience': '5 years textile sales — Ring Road market',
                'why': 'Already sell to 40+ garment units. Want WB packages to offer as DGC.',
                'status': DgcApplication.STATUS_NEW,
                'days': 1,
            },
            {
                'name': 'Divya Menon',
                'email': 'divya.menon@demo.wb.in',
                'phone': '9847011223',
                'city': 'Tirupur',
                'experience': 'Freelance digital marketer for knitwear factories',
                'why': 'Clients keep asking for full store+ads setup. Partnering with WB makes sense.',
                'status': DgcApplication.STATUS_REVIEW,
                'days': 4,
            },
            {
                'name': 'Rajesh Choudhary',
                'email': 'rajesh.c@demo.wb.in',
                'phone': '9414012345',
                'city': 'Jaipur',
                'experience': 'Block-print wholesaler network',
                'why': 'Want to help Rajasthan printers go prepaid D2C.',
                'status': DgcApplication.STATUS_NEW,
                'days': 2,
            },
        ]
        for row in rows:
            days = row.pop('days')
            app, created = DgcApplication.objects.update_or_create(
                email=row['email'],
                defaults=row,
            )
            _backdate(DgcApplication, app.pk, days=days)
            self.stdout.write(f"  DGC app {'+' if created else '~'} {app.name} ({app.city})")

    def _seed_dgc_leads(self, partner):
        rows = [
            {
                'name': 'Manish Goenka',
                'email': 'manish.goenka@demo.wb.in',
                'phone': '9831011223',
                'company': 'Goenka Silk Mills',
                'interest': 'Startup D2C Launch',
                'notes': 'Referred via Ring Road contact. Ready for store + Meta kickoff.',
                'deal_value': Decimal('15000.00'),
                'status': PartnerLead.STATUS_NEW,
                'days': 0,
            },
            {
                'name': 'Kavita Shetty',
                'email': 'kavita.shetty@demo.wb.in',
                'phone': '9886012345',
                'company': 'Coastal Cotton Wear',
                'interest': 'Growth Ads Retainer',
                'notes': 'Bangalore-based cotton brand. Wants Meta + Google retainer.',
                'deal_value': Decimal('35000.00'),
                'status': PartnerLead.STATUS_CONTACTED,
                'days': 3,
            },
            {
                'name': 'Imran Shaikh',
                'email': 'imran.shaikh@demo.wb.in',
                'phone': '9892011122',
                'company': 'Shaikh Power Loom',
                'interest': 'Full F2C Scale',
                'notes': 'Bhiwandi unit. High volume — exploring Scale package.',
                'deal_value': Decimal('75000.00'),
                'status': PartnerLead.STATUS_NEW,
                'days': 1,
            },
            {
                'name': 'Lata Patel',
                'email': 'lata.patel@demo.wb.in',
                'phone': '9727712345',
                'company': 'Patel Dupatta Traders',
                'interest': 'Growth Ads Retainer',
                'notes': 'Won — prepaid store live, first ads week.',
                'deal_value': Decimal('35000.00'),
                'status': PartnerLead.STATUS_WON,
                'days': 18,
            },
        ]
        for row in rows:
            days = row.pop('days')
            lead, created = PartnerLead.objects.update_or_create(
                partner=partner,
                email=row['email'],
                defaults=row,
            )
            _backdate(PartnerLead, lead.pk, days=days)
            if lead.status == PartnerLead.STATUS_WON and lead.deal_value:
                Commission.objects.get_or_create(
                    partner=partner,
                    lead=lead,
                    defaults={
                        'amount': (lead.deal_value * Decimal('0.15')).quantize(Decimal('0.01')),
                        'source': Commission.SOURCE_LEAD,
                        'status': Commission.STATUS_PENDING,
                        'note': f'Demo commission — {lead.company}',
                    },
                )
            self.stdout.write(f"  DGC lead {'+' if created else '~'} {lead.name}")

    def _seed_payout(self, partner):
        month = PayoutRequest.month_start()
        payout, created = PayoutRequest.objects.get_or_create(
            partner=partner,
            period_month=month,
            defaults={
                'amount': Decimal('5250.00'),
                'status': PayoutRequest.STATUS_PENDING,
                'note': 'Demo payout request — commission on Patel Dupatta deal',
            },
        )
        self.stdout.write(f"  Payout {'+' if created else '~'} ₹{payout.amount} ({payout.status})")

    def _seed_clients_projects_billing(self, pm):
        clients = [
            {
                'username': 'client_demo_saree',
                'company': '[Demo] Shree Ambika Sarees',
                'industry': 'Textile — Sarees',
                'projects': [
                    ('[Demo] Ambika D2C Store + Meta Ads', 'Meta Ads', Project.STATUS_ACTIVE, 45),
                    ('[Demo] Ambika Catalog SEO', 'SEO', Project.STATUS_PLANNING, 10),
                ],
                'invoices': [
                    ('WB-DEMO-2001', 'Growth Retainer — June', Decimal('35000.00'), Invoice.STATUS_OVERDUE, -8),
                    ('WB-DEMO-2002', 'Store Setup Milestone', Decimal('45000.00'), Invoice.STATUS_SENT, 7),
                ],
            },
            {
                'username': 'client_demo_tees',
                'company': '[Demo] Tirupur Knit Factory',
                'industry': 'Garment — T-shirts',
                'projects': [
                    ('[Demo] Knit Factory Prepaid Store', 'eCommerce', Project.STATUS_ACTIVE, 70),
                ],
                'invoices': [
                    ('WB-DEMO-2003', 'Ads Management — July', Decimal('28000.00'), Invoice.STATUS_PAID, -2),
                    ('WB-DEMO-2004', 'WhatsApp Automation Setup', Decimal('18000.00'), Invoice.STATUS_SENT, 12),
                ],
            },
            {
                'username': 'client_demo_kurti',
                'company': '[Demo] Rangoli Kurtis',
                'industry': 'Ethnic Wear',
                'projects': [
                    ('[Demo] Rangoli Google Shopping', 'Google Ads', Project.STATUS_PLANNING, 5),
                ],
                'invoices': [
                    ('WB-DEMO-2005', 'Discovery + Proposal Fee', Decimal('10000.00'), Invoice.STATUS_OVERDUE, -3),
                ],
            },
        ]

        for data in clients:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': f"{data['username']}@demo.wb.in",
                    'first_name': data['company'].replace('[Demo] ', '').split()[0],
                },
            )
            if created:
                user.set_password('demo1234')
                user.save()
            account, _ = ClientAccount.objects.get_or_create(
                user=user,
                defaults={
                    'company_name': data['company'],
                    'industry': data['industry'],
                    'account_manager': pm,
                },
            )
            # Keep company name in sync for demo tag
            if account.company_name != data['company']:
                account.company_name = data['company']
                account.industry = data['industry']
                account.save(update_fields=['company_name', 'industry'])

            first_project = None
            for name, service, status, progress in data['projects']:
                project, _ = Project.objects.update_or_create(
                    client_account=account,
                    name=name,
                    defaults={
                        'service_type': service,
                        'description': f'Demo F2C project for {data["company"]}.',
                        'status': status,
                        'progress_percent': progress,
                        'project_manager': pm,
                        'start_date': date.today() - timedelta(days=30),
                    },
                )
                if first_project is None:
                    first_project = project

            for inv_no, title, amount, status, due_offset in data['invoices']:
                Invoice.objects.update_or_create(
                    invoice_number=inv_no,
                    defaults={
                        'client_account': account,
                        'project': first_project,
                        'title': title,
                        'amount': amount,
                        'status': status,
                        'due_date': date.today() + timedelta(days=due_offset),
                        'notes': 'Demo invoice — Indian textile D2C context',
                    },
                )
            self.stdout.write(f"  Client ~ {data['company']}")

    def _seed_qa_deliverables(self, pm):
        project = Project.objects.filter(name__startswith='[Demo]').first()
        if not project:
            self.stdout.write(self.style.WARNING('No demo project for QA deliverables.'))
            return
        items = [
            ('Meta Ad Creatives Pack — Festive Sarees', '12 square + story creatives for Diwali push. Needs brand QA.'),
            ('WhatsApp Order SOP Document', 'Backoffice SOP for prepaid order desk — Hindi + English.'),
            ('Google Merchant Feed Draft', 'SKU feed for 480 saree variants — pending accuracy check.'),
        ]
        for title, desc in items:
            d, created = Deliverable.objects.get_or_create(
                project=project,
                title=title,
                defaults={
                    'description': desc,
                    'approval_status': Deliverable.APPROVAL_PENDING,
                },
            )
            self.stdout.write(f"  QA {'+' if created else '~'} {d.title}")
