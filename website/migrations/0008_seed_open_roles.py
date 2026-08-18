from django.db import migrations

ROLES = [
    {
        'slug': 'meta-ads-specialist',
        'title': 'Meta Ads Specialist',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Marketing',
        'summary': 'Run Facebook & Instagram campaigns for manufacturer D2C brands — creative testing, audiences, and ROAS.',
        'tags': ['Meta Ads', 'Creative', 'ROAS'],
    },
    {
        'slug': 'google-ads-specialist',
        'title': 'Google Ads / Shopping Specialist',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Marketing',
        'summary': 'Own search and shopping campaigns for high-SKU fashion catalogs with prepaid conversion goals.',
        'tags': ['PPC', 'Shopping', 'Analytics'],
    },
    {
        'slug': 'marketing-executive',
        'title': 'Marketing Executive',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Marketing',
        'summary': 'Own day-to-day brand marketing for textile D2C clients — campaigns, creatives briefs, WhatsApp promos, and weekly growth reporting.',
        'tags': ['Campaigns', 'D2C', 'Reporting'],
    },
    {
        'slug': 'seo-specialist',
        'title': 'SEO Specialist',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Marketing',
        'summary': 'Grow organic traffic for manufacturer storefronts — category pages, product SEO, local Surat signals, and content that converts.',
        'tags': ['SEO', 'Content', 'Organic'],
    },
    {
        'slug': 'content-email-strategist',
        'title': 'Content & Email Strategist',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Marketing',
        'summary': 'Write product stories, launch emails, and retention sequences that turn catalog browsers into prepaid buyers.',
        'tags': ['Content', 'Email', 'Retention'],
    },
    {
        'slug': 'whatsapp-commerce',
        'title': 'WhatsApp Commerce Specialist',
        'job_type': 'Full-time',
        'location': 'Surat',
        'department': 'Marketing',
        'summary': 'Build WhatsApp catalogs, abandoned-cart flows, and sales chat playbooks for factory D2C brands.',
        'tags': ['WhatsApp', 'CRM', 'Conversion'],
    },
    {
        'slug': 'graphic-designer',
        'title': 'Graphic Designer',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Creative',
        'summary': 'Design ad creatives, catalog visuals, and brand kits for fashion and textile D2C stores — fast turnaround, conversion-first.',
        'tags': ['Design', 'Ads', 'Brand'],
    },
    {
        'slug': 'frontend-ai-designer',
        'title': 'Frontend AI Designer',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Creative',
        'summary': 'Ship storefront UI with AI-assisted design — landing pages, product grids, and conversion layouts for manufacturer brands.',
        'tags': ['UI', 'AI Design', 'Frontend'],
    },
    {
        'slug': 'video-reels-creator',
        'title': 'Video / Reels Creator',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Creative',
        'summary': 'Produce short-form product and factory-story reels that feed Meta ads and organic social for D2C clients.',
        'tags': ['Reels', 'Video', 'Social'],
    },
    {
        'slug': 'fullstack-ecommerce',
        'title': 'Full-Stack / eCommerce Developer',
        'job_type': 'Full-time',
        'location': 'Surat / Remote',
        'department': 'Tech',
        'summary': 'Build and ship storefronts, dashboards, and automation that power client D2C operations.',
        'tags': ['Django', 'Frontend', 'eCommerce'],
    },
    {
        'slug': 'ai-automation-engineer',
        'title': 'AI Automation Engineer',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Tech',
        'summary': 'Design AI agents and no-code/low-code workflows for marketing, sales, support, and ops.',
        'tags': ['AI', 'Automation', 'n8n'],
    },
    {
        'slug': 'ops-crm-associate',
        'title': 'Operations / CRM Associate',
        'job_type': 'Full-time',
        'location': 'Surat',
        'department': 'Operations',
        'summary': 'SOPs, order workflows, WhatsApp support systems, and client backoffice training.',
        'tags': ['CRM', 'SOPs', 'CX'],
    },
    {
        'slug': 'backoffice-executive',
        'title': 'Backoffice Executive',
        'job_type': 'Full-time',
        'location': 'Surat',
        'department': 'Operations',
        'summary': 'Handle order entry, catalog updates, courier coordination, and day-to-day client backoffice for live D2C accounts.',
        'tags': ['Orders', 'Catalog', 'Logistics'],
    },
    {
        'slug': 'catalog-listing-executive',
        'title': 'Catalog / Listing Executive',
        'job_type': 'Full-time',
        'location': 'Surat',
        'department': 'Operations',
        'summary': 'Upload and optimise high-SKU textile catalogs — titles, variants, images, and pricing across client stores.',
        'tags': ['Catalog', 'SKU', 'eCommerce'],
    },
    {
        'slug': 'account-manager',
        'title': 'Account Manager',
        'job_type': 'Full-time',
        'location': 'Surat / Hybrid',
        'department': 'Client Success',
        'summary': 'Own manufacturer client relationships — weekly reviews, delivery coordination, and growth upsells across store, ads, and ops.',
        'tags': ['Clients', 'Delivery', 'Growth'],
    },
    {
        'slug': 'sales-executive',
        'title': 'Sales Executive (Manufacturer Acquisition)',
        'job_type': 'Full-time',
        'location': 'Surat / Field',
        'department': 'Sales',
        'summary': 'Close textile manufacturers on D2C packages — store setup, ads, and prepaid-order systems. Field + phone heavy.',
        'tags': ['Sales', 'B2B', 'D2C'],
    },
    {
        'slug': 'growth-intern',
        'title': 'Growth Intern (Marketing / Ops / Dev)',
        'job_type': 'Internship',
        'location': 'Surat / Hybrid',
        'department': 'Internship',
        'summary': 'Work on real client projects under seniors — portfolio, mentorship, and path to full-time.',
        'tags': ['Internship', 'Mentorship', 'Real projects'],
    },
]


def seed_roles(apps, schema_editor):
    JobOpening = apps.get_model('website', 'JobOpening')
    for role in ROLES:
        JobOpening.objects.get_or_create(slug=role['slug'], defaults=role)


def unseed_roles(apps, schema_editor):
    JobOpening = apps.get_model('website', 'JobOpening')
    JobOpening.objects.filter(slug__in=[r['slug'] for r in ROLES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_jobopening'),
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]
