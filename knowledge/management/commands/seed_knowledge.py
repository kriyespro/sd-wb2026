from django.core.management.base import BaseCommand
from django.utils.text import slugify

from knowledge.models import KnowledgeArticle


SEED = [
    {
        'title': 'Enquiry follow-up SOP',
        'category': 'Office',
        'audience': KnowledgeArticle.AUDIENCE_OFFICE,
        'summary': 'How office managers contact and qualify inbound enquiries.',
        'body': (
            '1. Assign the lead to yourself in /ops/leads/.\n'
            '2. Complete the follow-up checklist (call, WhatsApp, need confirm, quote, next date).\n'
            '3. Set next follow-up date on the Office desk.\n'
            '4. Move status: New → Contacted → Qualified → Proposal → Won/Lost.\n'
            '5. On Won, convert to client from the lead row.'
        ),
        'sort_order': 1,
    },
    {
        'title': 'Ecommerce Website package (₹15k/yr)',
        'category': 'Packages',
        'audience': KnowledgeArticle.AUDIENCE_ALL,
        'summary': 'Reseller cost ₹15,000/year — market sell ₹25k–₹30k.',
        'body': (
            'Includes domain, server setup, and full technical support.\n'
            'DGC places order from /dashboard/dgc/orders/.\n'
            'Ops confirms and assigns delivery in /ops/dgc-orders/.\n'
            'Delivery uses package SOP and uploads for QA.'
        ),
        'sort_order': 10,
    },
    {
        'title': 'Ecommerce Plus package (₹30k)',
        'category': 'Packages',
        'audience': KnowledgeArticle.AUDIENCE_ALL,
        'summary': 'Reseller cost ₹30,000 — market sell ₹45k–₹50k.',
        'body': (
            'Enhanced catalog, payments, growth-ready store.\n'
            'Includes domain, server, full technical support.\n'
            'Assign to web developer/freelancer after order confirm.'
        ),
        'sort_order': 11,
    },
    {
        'title': 'Dropshipping + Auto Reseller Stores (₹90k)',
        'category': 'Packages',
        'audience': KnowledgeArticle.AUDIENCE_ALL,
        'summary': 'Reseller cost ₹90,000 — market sell ₹120k–₹130k.',
        'body': (
            'Dropshipping ecommerce with auto reseller store create.\n'
            'Includes domain, server, full technical support.\n'
            'Delivery checklist: store base, reseller create flow, training handoff.'
        ),
        'sort_order': 12,
    },
    {
        'title': 'DGC order delivery handoff',
        'category': 'Delivery',
        'audience': KnowledgeArticle.AUDIENCE_DELIVERY,
        'summary': 'What freelancers/devs do after an order is assigned.',
        'body': (
            '1. Open My Work in /ops/my-work/.\n'
            '2. Read package notes and due date.\n'
            '3. Build deliverables; update work notes.\n'
            '4. Mark order Fulfilled when ready for QA / client handoff.\n'
            '5. Escalate blockers to PM/admin in ops.'
        ),
        'sort_order': 20,
    },
    {
        'title': 'DGC partner quick start',
        'category': 'DGC',
        'audience': KnowledgeArticle.AUDIENCE_DGC,
        'summary': 'How partners sell packages and submit leads.',
        'body': (
            '1. Review offers and your cost vs market sell.\n'
            '2. Place reseller orders from Orders.\n'
            '3. Submit factory leads from Leads.\n'
            '4. Track commissions and payouts.\n'
            '5. Use Knowledge Base for package talking points.'
        ),
        'sort_order': 30,
    },
]


class Command(BaseCommand):
    help = 'Seed OS Hub knowledge base articles'

    def handle(self, *args, **options):
        for data in SEED:
            slug = slugify(data['title'])[:220]
            obj, created = KnowledgeArticle.objects.update_or_create(
                slug=slug,
                defaults={**data, 'is_published': True},
            )
            self.stdout.write(f"{'Created' if created else 'Updated'}: {obj.title}")
        self.stdout.write(self.style.SUCCESS('Knowledge base seeded.'))
