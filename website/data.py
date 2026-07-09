from urllib.parse import quote


def ph(w, h, label, bg='EEF2F9', fg='1E3A6E'):
    return f'https://placehold.co/{w}x{h}/{bg}/{fg}?text={quote(label)}&font=roboto'


def img(photo, w=1200, h=800):
    """Free Unsplash stock image (https://unsplash.com/license)."""
    return f'https://images.unsplash.com/{photo}?auto=format&fit=crop&w={w}&h={h}&q=80'


SITE_IMAGES = {
    'hero': img('photo-1460925895917-afdab827c52f', 640, 420),
    'contact_bg': img('photo-1497366216548-37526070297c', 1920, 900),
    'about_team': img('photo-1522071820081-009f0129c71c', 900, 700),
}

MODEL_STEPS = [
    {
        'title': 'Digital Growth Company',
        'desc': 'What clients see and hire — a full-service growth partner across SEO, ads, web, and automation.',
        'image': img('photo-1556761175-5973dc0f32e7', 900, 600),
    },
    {
        'title': 'Internal Academy',
        'desc': 'A talent development system that trains future specialists on real client work — not the headline.',
        'image': img('photo-1524178232363-1fb2b075b655', 900, 600),
    },
    {
        'title': 'Better Delivery',
        'desc': 'Skilled teams, lower overhead, higher client satisfaction — the result of the two systems working together.',
        'image': img('photo-1600880292203-757bb62b4baf', 900, 600),
    },
]

SERVICES = [
    {
        'slug': 'seo',
        'title': 'SEO',
        'icon': '🔍',
        'short': 'Rank higher on Google and drive organic traffic that converts.',
        'description': (
            'We build sustainable search visibility through technical SEO, '
            'content strategy, and authority building tailored to your market.'
        ),
        'gallery': [
            img('photo-1432888498266-38ff6183fd6a', 1200, 800),
            img('photo-1551288049-bebda4e38f71', 1200, 800),
        ],
    },
    {
        'slug': 'google-ads',
        'title': 'Google Ads',
        'icon': '📈',
        'short': 'Capture high-intent leads with data-driven paid search campaigns.',
        'description': (
            'From keyword research to landing page optimization, we manage '
            'Google Ads campaigns focused on ROI and measurable growth.'
        ),
        'gallery': [
            img('photo-1556761175-b1176c4bbf9b', 1200, 800),
            img('photo-1460925895917-afdab827c52f', 1200, 800),
        ],
    },
    {
        'slug': 'meta-ads',
        'title': 'Meta Ads',
        'icon': '📱',
        'short': 'Scale brand awareness and conversions across Facebook & Instagram.',
        'description': (
            'Creative-first Meta campaigns with precise audience targeting, '
            'retargeting funnels, and performance reporting you can trust.'
        ),
        'gallery': [
            img('photo-1611162616305-c69b3fa7fbe0', 1200, 800),
            img('photo-1563986768609-322da13575f3', 1200, 800),
        ],
    },
    {
        'slug': 'website-development',
        'title': 'Website Development',
        'icon': '💻',
        'short': 'Fast, modern websites built to convert visitors into customers.',
        'description': (
            'Custom websites and landing pages with clean UX, mobile-first '
            'design, and SEO-ready architecture from day one.'
        ),
        'gallery': [
            img('photo-1467232004584-a241de8bcf5d', 1200, 800),
            img('photo-1547658719-da2b51169166', 1200, 800),
        ],
    },
    {
        'slug': 'automation',
        'title': 'Automation',
        'icon': '⚡',
        'short': 'Automate repetitive tasks and scale operations with AI workflows.',
        'description': (
            'We connect your tools, automate lead flows, and build AI-powered '
            'workflows that save time and reduce manual errors.'
        ),
        'gallery': [
            img('photo-1518186285589-2f7649de56e0', 1200, 800),
            img('photo-1485827404703-89b55fcc595e', 1200, 800),
        ],
    },
    {
        'slug': 'crm',
        'title': 'CRM',
        'icon': '🗂️',
        'short': 'Organize leads, pipelines, and customer relationships in one place.',
        'description': (
            'CRM setup, customization, and integration so your sales and '
            'marketing teams work from a single source of truth.'
        ),
        'gallery': [
            img('photo-1552664730-d307ca884978', 1200, 800),
            img('photo-1553877522-43269d4ea984', 1200, 800),
        ],
    },
    {
        'slug': 'branding',
        'title': 'Branding',
        'icon': '🎨',
        'short': 'Build a memorable brand identity that stands out in your market.',
        'description': (
            'Logo, visual identity, messaging, and brand guidelines that '
            'position your business as a trusted industry leader.'
        ),
        'gallery': [
            img('photo-1561070791-2526d30994b5', 1200, 800),
            img('photo-1626785774573-4b799315345d', 1200, 800),
        ],
    },
    {
        'slug': 'content-marketing',
        'title': 'Content Marketing',
        'icon': '✍️',
        'short': 'Content that educates, engages, and drives qualified leads.',
        'description': (
            'Blog posts, social content, email campaigns, and thought '
            'leadership crafted to attract and nurture your ideal customers.'
        ),
        'gallery': [
            img('photo-1455390582261-044cdead277a', 1200, 800),
            img('photo-1504868584819-f8e8b4b6d7e3', 1200, 800),
        ],
    },
]

WHY_CHOOSE_US = [
    {'title': 'Experienced Team', 'desc': 'Senior specialists across SEO, ads, dev, and design.'},
    {'title': 'Transparent Reporting', 'desc': 'Clear dashboards and monthly performance reviews.'},
    {'title': 'ROI Focused', 'desc': 'Every campaign tied to measurable business outcomes.'},
    {'title': 'Dedicated Project Manager', 'desc': 'One point of contact from kickoff to delivery.'},
    {'title': 'Industry Experts', 'desc': 'Domain knowledge across B2B, SaaS, e-commerce, and local.'},
]

RECENT_PROJECTS = [
    {
        'title': 'E-commerce Website Redesign', 'category': 'Website',
        'result': '+42% conversion rate', 'image': img('photo-1556742049-0cfed4f6a45d', 800, 600),
    },
    {
        'title': 'Local SEO Domination', 'category': 'SEO',
        'result': '3x organic traffic in 6 months', 'image': img('photo-1432888498266-38ff6183fd6a', 800, 600),
    },
    {
        'title': 'B2B Lead Generation Funnel', 'category': 'Lead Generation',
        'result': '120 qualified leads/month', 'image': img('photo-1552664730-d307ca884978', 800, 600),
    },
    {
        'title': 'AI Customer Support Bot', 'category': 'AI Chatbot',
        'result': '60% ticket deflection', 'image': img('photo-1677442136019-21780ecad995', 800, 600),
    },
    {
        'title': 'Sales Pipeline Automation', 'category': 'Automation',
        'result': '15 hrs/week saved', 'image': img('photo-1518186285589-2f7649de56e0', 800, 600),
    },
]

SERVICE_PROCESS = [
    {'title': 'Discover & Strategize', 'desc': 'We audit your market, goals, and funnels to build a growth roadmap.'},
    {'title': 'Build & Execute', 'desc': 'Our specialists launch campaigns, sites, and systems on that roadmap.'},
    {'title': 'Optimize & Scale', 'desc': 'We track results monthly and double down on what drives revenue.'},
]

TEAM_ROLES = [
    {'role': 'Project Managers', 'count': '4', 'image': img('photo-1560250097-0b93528c311a', 200, 200)},
    {'role': 'SEO Specialists', 'count': '6', 'image': img('photo-1507003211169-0a1dd7228f2d', 200, 200)},
    {'role': 'Developers', 'count': '8', 'image': img('photo-1519085362263-aa42b02f1f9c', 200, 200)},
    {'role': 'Designers', 'count': '5', 'image': img('photo-1494790108377-be9c29b29330', 200, 200)},
    {'role': 'Media Buyers', 'count': '4', 'image': img('photo-1500648767791-00dcc994a43e', 200, 200)},
]

CASE_STUDIES = [
    {
        'slug': 'saas-seo-growth',
        'title': 'SaaS SEO Growth',
        'category': 'SEO',
        'client': 'B2B SaaS Platform',
        'result': '250% increase in organic signups',
        'summary': 'Full technical audit, content hub strategy, and link building over 8 months.',
        'image': img('photo-1432888498266-38ff6183fd6a', 800, 600),
        'impact_areas': ['Organic Traffic', 'Signups', 'Domain Authority'],
        'gallery': [
            img('photo-1551288049-bebda4e38f71', 1600, 900),
            img('photo-1460925895917-afdab827c52f', 1600, 900),
            img('photo-1556761175-b1176c4bbf9b', 1600, 900),
        ],
        'narrative': [
            {'heading': 'The Challenge', 'body': 'Organic signups had plateaued and technical debt was capping crawl efficiency across the product marketing site.'},
            {'heading': 'The Approach', 'body': 'We ran a full technical SEO audit, rebuilt the content hub around buyer-intent keywords, and executed a targeted link-building campaign.'},
            {'heading': 'The Result', 'body': 'Organic signups grew 250% within 8 months, with sustained month-over-month gains after the campaign ended.'},
        ],
    },
    {
        'slug': 'ecommerce-meta-ads',
        'title': 'E-commerce Meta Ads Scale',
        'category': 'Meta Ads',
        'client': 'D2C Fashion Brand',
        'result': '4.2x ROAS at scale',
        'summary': 'Creative testing framework and lookalike audience expansion.',
        'image': img('photo-1441986300917-64674bd600d8', 800, 600),
        'impact_areas': ['ROAS', 'Creative Testing', 'Audience Expansion'],
        'gallery': [
            img('photo-1611162616305-c69b3fa7fbe0', 1600, 900),
            img('photo-1563986768609-322da13575f3', 1600, 900),
            img('photo-1556742049-0cfed4f6a45d', 1600, 900),
        ],
        'narrative': [
            {'heading': 'The Challenge', 'body': 'Rising CPMs were eroding margins as the brand tried to scale past its early lookalike audiences.'},
            {'heading': 'The Approach', 'body': 'We built a systematic creative testing framework and layered in fresh lookalike and interest-based audience segments.'},
            {'heading': 'The Result', 'body': 'ROAS climbed to 4.2x even as monthly spend scaled 3x, with creative fatigue kept in check by the testing cadence.'},
        ],
    },
    {
        'slug': 'local-lead-gen',
        'title': 'Local Lead Generation',
        'category': 'Google Ads',
        'client': 'Home Services Company',
        'result': '85 leads/month at ₹420 CPL',
        'summary': 'Geo-targeted campaigns with call tracking and landing page optimization.',
        'image': img('photo-1503387762-592deb58ef4e', 800, 600),
        'impact_areas': ['Cost Per Lead', 'Call Volume', 'Local Coverage'],
        'gallery': [
            img('photo-1560518883-ce09059eeffa', 1600, 900),
            img('photo-1553877522-43269d4ea984', 1600, 900),
            img('photo-1552664730-d307ca884978', 1600, 900),
        ],
        'narrative': [
            {'heading': 'The Challenge', 'body': 'Lead volume was inconsistent and cost per lead was too high to profitably scale across service areas.'},
            {'heading': 'The Approach', 'body': 'We rebuilt geo-targeted campaign structures, added call tracking, and optimized landing pages for each service area.'},
            {'heading': 'The Result', 'body': 'The client now gets 85 qualified leads a month at ₹420 CPL, with predictable month-over-month volume.'},
        ],
    },
    {
        'slug': 'automation-crm',
        'title': 'CRM & Automation Overhaul',
        'category': 'Automation',
        'client': 'Real Estate Agency',
        'result': '40% faster lead response time',
        'summary': 'HubSpot setup with automated nurture sequences and lead scoring.',
        'image': img('photo-1560518883-ce09059eeffa', 800, 600),
        'impact_areas': ['Response Time', 'Lead Scoring', 'Pipeline Visibility'],
        'gallery': [
            img('photo-1553877522-43269d4ea984', 1600, 900),
            img('photo-1518186285589-2f7649de56e0', 1600, 900),
            img('photo-1552664730-d307ca884978', 1600, 900),
        ],
        'narrative': [
            {'heading': 'The Challenge', 'body': 'Leads were falling through the cracks between multiple spreadsheets and no consistent scoring or follow-up process.'},
            {'heading': 'The Approach', 'body': 'We stood up HubSpot as the single source of truth, built automated nurture sequences, and layered in lead scoring.'},
            {'heading': 'The Result', 'body': 'Lead response time dropped 40% and the sales team now trusts the pipeline enough to forecast off it.'},
        ],
    },
]

INDUSTRIES = [
    {'title': 'SaaS & Technology', 'desc': 'Growth strategies for product-led and sales-led SaaS companies.', 'icon': '🚀'},
    {'title': 'E-commerce', 'desc': 'Conversion-focused ads, SEO, and storefront optimization.', 'icon': '🛒'},
    {'title': 'Healthcare', 'desc': 'Compliant digital marketing for clinics and health brands.', 'icon': '🏥'},
    {'title': 'Real Estate', 'desc': 'Lead generation and CRM automation for agencies and builders.', 'icon': '🏘️'},
    {'title': 'Education', 'desc': 'Enrollment campaigns and brand building for institutes.', 'icon': '🎓'},
    {'title': 'Local Business', 'desc': 'Local SEO, Google Business Profile, and hyper-local ads.', 'icon': '📍'},
]

PRICING_TIERS = [
    {
        'name': 'Starter',
        'price': '₹25,000',
        'price_monthly': '₹25,000',
        'price_annual': '₹22,500',
        'period': '/month',
        'features': ['1 service channel', 'Monthly reporting', 'Email support', 'Dedicated PM'],
        'highlight': False,
    },
    {
        'name': 'Growth',
        'price': '₹55,000',
        'price_monthly': '₹55,000',
        'price_annual': '₹49,500',
        'period': '/month',
        'features': ['3 service channels', 'Bi-weekly strategy calls', 'Priority support', 'Custom dashboards'],
        'highlight': True,
    },
    {
        'name': 'Enterprise',
        'price': 'Custom',
        'price_monthly': 'Custom',
        'price_annual': 'Custom',
        'period': '',
        'features': ['Full-service growth', 'Weekly strategy calls', 'Dedicated senior team', 'SLA & custom reporting'],
        'highlight': False,
    },
]

PRICING_FAQS = [
    {'q': 'Can I switch plans later?', 'a': 'Yes — upgrade or downgrade anytime; changes apply from your next billing cycle.'},
    {'q': 'Is there a setup fee?', 'a': 'No setup fees on any plan. You only pay the listed monthly or annual rate.'},
    {'q': 'What does annual billing save me?', 'a': 'Annual billing is discounted roughly 10% compared to paying monthly.'},
    {'q': 'Do you offer custom scopes?', 'a': 'Yes — Enterprise plans are scoped around your specific channels and team size.'},
    {'q': 'What is the minimum contract length?', 'a': 'Month-to-month on Starter and Growth; Enterprise contracts are typically 6-12 months.'},
]

ACADEMY_PROCESS = [
    'Admission', 'Training', 'Assessment', 'Internal Internship',
    'Client Project', 'Portfolio', 'Placement',
]

# Animated counters (integers so they count up cleanly)
STATS = [
    {'value': 120, 'suffix': '+', 'label': 'Projects Delivered'},
    {'value': 94, 'suffix': '%', 'label': 'Client Retention'},
    {'value': 27, 'suffix': '', 'label': 'Experts On Team'},
    {'value': 15, 'suffix': '+', 'label': 'Industries Served'},
]

CLIENT_LOGOS = [
    {'name': 'Google', 'image': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg'},
    {'name': 'Amazon', 'image': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg'},
    {'name': 'Apple', 'image': 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg'},
    {'name': 'Microsoft', 'image': 'https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg'},
    {'name': 'Netflix', 'image': 'https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg'},
    {'name': 'Spotify', 'image': 'https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg'},
    {'name': 'Adobe', 'image': 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Adobe_Corporate_logo.svg'},
    {'name': 'Slack', 'image': 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg'},
]

INSTAGRAM_IMAGES = [
    img('photo-1611162616305-c69b3fa7fbe0', 400, 400),
    img('photo-1556742049-0cfed4f6a45d', 400, 400),
    img('photo-1460925895917-afdab827c52f', 400, 400),
    img('photo-1551288049-bebda4e38f71', 400, 400),
    img('photo-1522071820081-009f0129c71c', 400, 400),
    img('photo-1561070791-2526d30994b5', 400, 400),
    img('photo-1455390582261-044cdead277a', 400, 400),
    img('photo-1518186285589-2f7649de56e0', 400, 400),
]

CONTACT_INFO = {
    'email': 'hello@winningblueprints.com',
    'phone': '+91 98765 43210',
    'address': 'HSR Layout, Bengaluru, India',
    'hours': 'Mon–Fri, 9am–6pm IST',
}

TESTIMONIALS = [
    {
        'quote': (
            'Winning Blueprints became a true growth partner. In six months our '
            'organic signups grew 2.5x and every report tied straight back to revenue.'
        ),
        'name': 'Priya Nair',
        'role': 'Head of Marketing',
        'company': 'B2B SaaS Platform',
        'initials': 'PN',
        'photo': img('photo-1573496359142-b8d87734a5a2', 120, 120),
    },
    {
        'quote': (
            'The paid team scaled our Meta ads to 4.2x ROAS without losing efficiency. '
            'Clear communication and a dedicated PM made all the difference.'
        ),
        'name': 'Arjun Mehta',
        'role': 'Founder',
        'company': 'D2C Fashion Brand',
        'initials': 'AM',
        'photo': img('photo-1472099645785-5658abf4ff4e', 120, 120),
    },
    {
        'quote': (
            'They rebuilt our website and automated our lead flow. Response time dropped '
            '40% and our sales team finally trusts the pipeline.'
        ),
        'name': 'Sara Williams',
        'role': 'Operations Director',
        'company': 'Real Estate Agency',
        'initials': 'SW',
        'photo': img('photo-1580489944761-15a19d654956', 120, 120),
    },
]
