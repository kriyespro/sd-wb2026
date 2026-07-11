from urllib.parse import quote


def ph(w, h, label, bg='EEF2F9', fg='1E3A6E'):
    return f'https://placehold.co/{w}x{h}/{bg}/{fg}?text={quote(label)}&font=roboto'


def img(photo, w=1200, h=800):
    """Free Unsplash stock image (https://unsplash.com/license)."""
    return f'https://images.unsplash.com/{photo}?auto=format&fit=crop&w={w}&h={h}&q=80'


SITE_IMAGES = {
    'hero': img('photo-1558769132-cb1aea458c5e', 640, 420),
    'contact_bg': img('photo-1441986300917-64674bd600d8', 1920, 900),
    'about_team': img('photo-1556761175-5973dc0f32e7', 900, 700),
}

# Dual model: D2C agency clients see + Academy talent pipeline behind the scenes
MODEL_STEPS = [
    {
        'title': 'D2C Growth Agency',
        'desc': (
            'What manufacturers hire — store setup, Meta & Google ads, prepaid order systems, '
            'and backoffice SOPs that take factories direct to customers.'
        ),
        'image': img('photo-1441986300917-64674bd600d8', 900, 600),
    },
    {
        'title': 'Internal Academy',
        'desc': (
            'A talent development system that trains future specialists on real client work — '
            'not the headline clients see, but how we keep delivery sharp at scale.'
        ),
        'image': img('photo-1524178232363-1fb2b075b655', 900, 600),
    },
    {
        'title': 'Better Delivery',
        'desc': (
            'Skilled teams, lower overhead, higher client satisfaction — the result of the '
            'agency + academy systems working together.'
        ),
        'image': img('photo-1600880292203-757bb62b4baf', 900, 600),
    },
]

F2C_PIPELINE = [
    {
        'title': 'Store Setup',
        'desc': 'Branded online store with mobile-first design, catalog, cart, and checkout.',
    },
    {
        'title': 'Traffic & Ads',
        'desc': 'Meta & Google ads targeting real buyers — not vanity reach.',
    },
    {
        'title': 'Prepaid Orders',
        'desc': 'Full payment before dispatch — zero credit risk, daily cash flow.',
    },
    {
        'title': 'Scale & Profit',
        'desc': '2x–4x margins, repeat customers, and a brand you own.',
    },
]

# Flagship packages shown on home (maps to detailed SERVICES)
FLAGSHIP_OFFERS = [
    {
        'title': 'eCommerce Setup',
        'icon': '🏪',
        'short': 'Branded store for B2C and bulk/wholesale (B2B) orders.',
        'features': ['Tailored storefront', 'Full catalog control', 'Mobile-first, sales-ready'],
        'slug': 'website-development',
        'popular': False,
    },
    {
        'title': 'Digital Marketing',
        'icon': '📱',
        'short': 'Meta, Google, WhatsApp & email that bring real prepaid buyers.',
        'features': ['Meta & Google ads setup', 'WhatsApp + email automation', 'Performance tracking & ROI'],
        'slug': 'meta-ads',
        'popular': True,
    },
    {
        'title': 'Backoffice Setup',
        'icon': '🗂️',
        'short': 'Train your staff to run orders, support, inventory, and returns.',
        'features': ['Team training & SOPs', 'Tool & dashboard setup', 'Daily operations setup'],
        'slug': 'crm',
        'popular': False,
    },
]

SERVICES = [
    {
        'slug': 'website-development',
        'title': 'eCommerce & Website',
        'icon': '💻',
        'short': 'Branded online stores built for textile catalogs and prepaid checkout.',
        'description': (
            'We build mobile-first storefronts with product pages, categories, cart, and checkout — '
            'ready for sarees, kurtis, t-shirts, jeans, and high-SKU fashion inventory. Supports both '
            'direct-to-customer (B2C) and bulk/wholesale (B2B) orders.'
        ),
        'gallery': [
            img('photo-1467232004584-a241de8bcf5d', 1200, 800),
            img('photo-1556742049-0cfed4f6a45d', 1200, 800),
        ],
    },
    {
        'slug': 'meta-ads',
        'title': 'Meta Ads',
        'icon': '📱',
        'short': 'Facebook & Instagram ads that generate daily prepaid orders for factories.',
        'description': (
            'Creative-first Meta campaigns using interests, behavior, and lookalike audiences — '
            'built to get real buyers for sarees, kurtis, t-shirts, and garment brands.'
        ),
        'gallery': [
            img('photo-1611162616305-c69b3fa7fbe0', 1200, 800),
            img('photo-1563986768609-322da13575f3', 1200, 800),
        ],
    },
    {
        'slug': 'google-ads',
        'title': 'Google Ads',
        'icon': '📈',
        'short': 'High-intent search and shopping ads for ready-to-buy customers.',
        'description': (
            'We set up search and shopping campaigns that capture customers already looking for '
            'your products — focused on prepaid conversions and measurable ROI.'
        ),
        'gallery': [
            img('photo-1556761175-b1176c4bbf9b', 1200, 800),
            img('photo-1460925895917-afdab827c52f', 1200, 800),
        ],
    },
    {
        'slug': 'seo',
        'title': 'SEO',
        'icon': '🔍',
        'short': 'Organic visibility so buyers find your brand without paid spend alone.',
        'description': (
            'Technical SEO, product/category content, and authority building tailored for '
            'fashion and textile D2C brands that need lasting organic demand.'
        ),
        'gallery': [
            img('photo-1432888498266-38ff6183fd6a', 1200, 800),
            img('photo-1551288049-bebda4e38f71', 1200, 800),
        ],
    },
    {
        'slug': 'automation',
        'title': 'WhatsApp & Automation',
        'icon': '⚡',
        'short': 'Cart recovery, order updates, and lead flows on WhatsApp & email.',
        'description': (
            'We connect your store, ads, and messaging tools so abandoned carts recover, '
            'orders update automatically, and your team spends less time on manual follow-ups.'
        ),
        'gallery': [
            img('photo-1518186285589-2f7649de56e0', 1200, 800),
            img('photo-1485827404703-89b55fcc595e', 1200, 800),
        ],
    },
    {
        'slug': 'crm',
        'title': 'Backoffice & CRM',
        'icon': '🗂️',
        'short': 'SOPs, dashboards, and CRM so your factory runs D2C like a machine.',
        'description': (
            'Order management, customer support workflows, inventory visibility, and CRM setup — '
            'plus training so your staff can run day-to-day operations without us in the room.'
        ),
        'gallery': [
            img('photo-1552664730-d307ca884978', 1200, 800),
            img('photo-1553877522-43269d4ea984', 1200, 800),
        ],
    },
    {
        'slug': 'branding',
        'title': 'Brand Identity',
        'icon': '🎨',
        'short': 'A brand customers trust — so you stop depending on traders.',
        'description': (
            'Logo, visual identity, messaging, and creatives that position your factory as a '
            'direct-to-customer brand customers remember and reorder from.'
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
        'short': 'Product stories and social content that educate and convert buyers.',
        'description': (
            'Catalog copy, social creatives, email sequences, and product storytelling crafted '
            'for textile and garment brands selling direct online.'
        ),
        'gallery': [
            img('photo-1455390582261-044cdead277a', 1200, 800),
            img('photo-1504868584819-f8e8b4b6d7e3', 1200, 800),
        ],
    },
]

WHY_CHOOSE_US = [
    {
        'title': 'No More Credit Sales',
        'desc': 'Digital storefronts and prepaid systems so you get paid before dispatch — less risk, better cash flow.',
    },
    {
        'title': 'Higher Profit Margins',
        'desc': 'Remove wholesalers and distributors. Earn what your product is worth — often 2x–4x more.',
    },
    {
        'title': 'Tested Systems, Real Results',
        'desc': 'Field-tested with real factories. Store, ads, and ops systems built to scale.',
    },
    {
        'title': 'Brand Control, Market Freedom',
        'desc': 'Own the customer, the data, and the experience. Stop depending on traders.',
    },
]

HERO_POINTS = [
    'Keep up to 60% more profit',
    'Daily orders, full cash flow',
    'Build a brand customers love',
]

AUDIENCE_TAGS = [
    'Textile Manufacturers',
    'Garment Factories',
    'Saree Brands',
    'T-Shirt Makers',
    'Kurti Producers',
    'D2C Fashion',
    'Factory Owners',
]

RECENT_PROJECTS = [
    {
        'title': 'Saree Brand D2C Store',
        'category': 'eCommerce',
        'result': 'Prepaid orders in 45 days',
        'image': img('photo-1610030469983-98e550d6193c', 800, 600),
    },
    {
        'title': 'T-Shirt Factory Meta Ads',
        'category': 'Meta Ads',
        'result': '3x margin vs wholesale',
        'image': img('photo-1523381210131-f77ef81b785a', 800, 600),
    },
    {
        'title': 'Kurti Brand Google Shopping',
        'category': 'Google Ads',
        'result': 'Daily high-intent buyers',
        'image': img('photo-1483985988355-763728e1935b', 800, 600),
    },
    {
        'title': 'Factory Backoffice SOPs',
        'category': 'Operations',
        'result': 'Team runs orders in-house',
        'image': img('photo-1552664730-d307ca884978', 800, 600),
    },
    {
        'title': 'WhatsApp Cart Recovery',
        'category': 'Automation',
        'result': '65% abandon recovery lift',
        'image': img('photo-1518186285589-2f7649de56e0', 800, 600),
    },
]

SERVICE_PROCESS = F2C_PIPELINE

TEAM_FOUNDERS = [
    {
        'name': 'Singh Kriti',
        'role': 'Operations Head & D2C Strategy Lead',
        'tags': ['D2C Strategy', 'Operations', 'Sales Systems'],
        'initials': 'SK',
        'bio': (
            '12+ years in textile D2C strategy. Singh Kriti has personally guided 200+ manufacturers '
            'from wholesale dependency to profitable direct sales — building brands that customers love.'
        ),
        'image': img('photo-1573496359142-b8d87734a5a2', 600, 600),
    },
    {
        'name': 'Kr. Sunil Verma',
        'role': 'Founder & CEO',
        'tags': ['AI Automation Engineer', 'Tech Architecture', 'eCommerce'],
        'initials': 'SV',
        'bio': (
            'Founder & CEO and AI Automation Engineer with a decade of eCommerce experience. '
            'Sunil architects the digital infrastructure and AI automation that powers every client’s '
            'D2C operation — from store to analytics.'
        ),
        'image': img('photo-1472099645785-5658abf4ff4e', 600, 600),
    },
]

TEAM_CORE = [
    {
        'name': 'ShreeVastav Mayank',
        'role': 'Marketing Expert',
        'tags': ['Meta Ads', 'SEO'],
        'initials': 'SM',
        'bio': 'Runs Meta and organic programs that bring real buyers — not empty traffic.',
        'image': img('photo-1507003211169-0a1dd7228f2d', 400, 400),
    },
    {
        'name': 'Dutta Anubhav',
        'role': 'Operations Head',
        'tags': ['Ops', 'CRM'],
        'initials': 'DA',
        'bio': 'SOPs, CRM, and backoffice workflows so your team can run D2C day-to-day.',
        'image': img('photo-1500648767791-00dcc994a43e', 400, 400),
    },
    {
        'name': 'Neha Rawat',
        'role': 'Creative Director',
        'tags': ['Design', 'Brand'],
        'initials': 'NR',
        'bio': 'Brand systems and creatives that make factory products feel like consumer brands.',
        'image': img('photo-1494790108377-be9c29b29330', 400, 400),
    },
    {
        'name': 'Arjun Kaushik',
        'role': 'Google Ads Lead',
        'tags': ['PPC', 'Shopping'],
        'initials': 'AK',
        'bio': 'High-intent search and shopping campaigns for ready-to-buy customers.',
        'image': img('photo-1519085362263-aa42b02f1f9c', 400, 400),
    },
    {
        'name': 'Priya Sharma',
        'role': 'Content Strategist',
        'tags': ['Content', 'Email'],
        'initials': 'PS',
        'bio': 'Product stories, email sequences, and catalog copy that convert browsers into buyers.',
        'image': img('photo-1580489944761-15a19d654956', 400, 400),
    },
    {
        'name': 'Ravi Verma',
        'role': 'Logistics Manager',
        'tags': ['Logistics', '3PL'],
        'initials': 'RV',
        'bio': 'Dispatch, 3PL, and fulfillment workflows that keep prepaid orders moving on time.',
        'image': img('photo-1560250097-0b93528c311a', 400, 400),
    },
    {
        'name': 'Sneha Gupta',
        'role': 'Customer Success',
        'tags': ['Support', 'CX'],
        'initials': 'SG',
        'bio': 'Post-purchase support and CX systems that turn first orders into repeat buyers.',
        'image': img('photo-1438761681033-6461ffad8d80', 400, 400),
    },
    {
        'name': 'Mohit Jain',
        'role': 'Analytics Lead',
        'tags': ['Data', 'ROI'],
        'initials': 'MJ',
        'bio': 'Dashboards and ROI tracking so every rupee of ad spend is accountable.',
        'image': img('photo-1506794778202-cad84cf45f1d', 400, 400),
    },
]

# Home / about preview — founders + first two core
TEAM = TEAM_FOUNDERS + TEAM_CORE[:2]

TEAM_DEPARTMENTS = [
    {
        'icon': '🛒',
        'title': 'eCommerce Team',
        'count': '25',
        'desc': 'Store designers, developers, and catalog managers who build high-converting D2C storefronts.',
    },
    {
        'icon': '📣',
        'title': 'Digital Marketing Team',
        'count': '35',
        'desc': 'Meta, Google, WhatsApp, and email specialists driving real buyers to your store every day.',
    },
    {
        'icon': '⚙️',
        'title': 'Operations Team',
        'count': '20',
        'desc': 'Backoffice trainers, SOP builders, and logistics coordinators keeping your D2C running smoothly.',
    },
    {
        'icon': '📊',
        'title': 'Analytics & Strategy',
        'count': '20',
        'desc': 'Data analysts and growth strategists constantly optimising campaigns, margins, and revenue.',
    },
]

# Kept for careers / capacity display
TEAM_ROLES = [
    {'role': 'Strategy & Sales', 'count': '4', 'image': img('photo-1560250097-0b93528c311a', 200, 200)},
    {'role': 'Ads & SEO', 'count': '6', 'image': img('photo-1507003211169-0a1dd7228f2d', 200, 200)},
    {'role': 'Developers', 'count': '8', 'image': img('photo-1519085362263-aa42b02f1f9c', 200, 200)},
    {'role': 'Designers', 'count': '5', 'image': img('photo-1494790108377-be9c29b29330', 200, 200)},
    {'role': 'Ops & CRM', 'count': '4', 'image': img('photo-1500648767791-00dcc994a43e', 200, 200)},
]

CASE_STUDIES = [
    {
        'slug': 'saree-manufacturer-d2c',
        'title': 'From 10% Margins to 3x Profit',
        'category': 'D2C Transformation',
        'client': 'Saree Manufacturer, Surat',
        'result': '3x margins with daily prepaid orders',
        'summary': (
            'Moved a Surat saree manufacturer from wholesale credit sales to a branded D2C store '
            'with Meta ads and prepaid checkout.'
        ),
        'image': img('photo-1610030469983-98e550d6193c', 800, 600),
        'impact_areas': ['Profit Margins', 'Prepaid Orders', 'Brand Ownership'],
        'gallery': [
            img('photo-1610030469983-98e550d6193c', 1600, 900),
            img('photo-1556742049-0cfed4f6a45d', 1600, 900),
            img('photo-1441986300917-64674bd600d8', 1600, 900),
        ],
        'narrative': [
            {
                'heading': 'The Challenge',
                'body': (
                    'Wholesale rates left barely 10% margin. Credit sales, distributors, and delays '
                    'controlled cash flow — the factory owned production but not the customer.'
                ),
            },
            {
                'heading': 'The Approach',
                'body': (
                    'We launched a branded store, ran Meta ads to real buyers, and set up prepaid '
                    'checkout plus WhatsApp order workflows so payment came before dispatch.'
                ),
            },
            {
                'heading': 'The Result',
                'body': (
                    'Margins rose ~3x. Daily prepaid orders replaced credit risk. The manufacturer '
                    'now owns the brand, the data, and the relationship with end customers.'
                ),
            },
        ],
    },
    {
        'slug': 'tshirt-factory-meta-ads',
        'title': 'T-Shirt Factory: Orders in 45 Days',
        'category': 'Meta Ads',
        'client': 'T-Shirt Factory, Tirupur',
        'result': 'Daily prepaid orders within 45 days',
        'summary': (
            'Store setup + Meta ads took a Tirupur t-shirt factory from distributor dependency '
            'to daily prepaid D2C orders.'
        ),
        'image': img('photo-1523381210131-f77ef81b785a', 800, 600),
        'impact_areas': ['Time to Orders', 'Cash Flow', 'No Middlemen'],
        'gallery': [
            img('photo-1523381210131-f77ef81b785a', 1600, 900),
            img('photo-1611162616305-c69b3fa7fbe0', 1600, 900),
            img('photo-1563986768609-322da13575f3', 1600, 900),
        ],
        'narrative': [
            {
                'heading': 'The Challenge',
                'body': (
                    'Stuck in the traditional model — distributors, credit, and delays. No direct '
                    'path to end customers or predictable prepaid revenue.'
                ),
            },
            {
                'heading': 'The Approach',
                'body': (
                    'We set up the store, launched Facebook & Instagram campaigns, and trained the '
                    'team on order handling so fulfillment stayed inside the factory.'
                ),
            },
            {
                'heading': 'The Result',
                'body': (
                    'Within 45 days, daily prepaid orders were flowing. No credit, no middlemen — '
                    'profit straight to the factory.'
                ),
            },
        ],
    },
    {
        'slug': 'kurti-brand-google-shopping',
        'title': 'Kurti Brand Google Shopping Scale',
        'category': 'Google Ads',
        'client': 'Ethnic Wear Brand',
        'result': 'High-intent buyers at profitable CPL',
        'summary': 'Shopping and search ads capturing ready-to-buy customers for ethnic wear SKUs.',
        'image': img('photo-1483985988355-763728e1935b', 800, 600),
        'impact_areas': ['Shopping Ads', 'Intent Traffic', 'Catalog Scale'],
        'gallery': [
            img('photo-1483985988355-763728e1935b', 1600, 900),
            img('photo-1460925895917-afdab827c52f', 1600, 900),
            img('photo-1556761175-b1176c4bbf9b', 1600, 900),
        ],
        'narrative': [
            {
                'heading': 'The Challenge',
                'body': 'Meta alone was not enough — high-intent search demand for kurtis and ethnic wear was going to competitors.',
            },
            {
                'heading': 'The Approach',
                'body': 'We structured Google Shopping and search campaigns around catalog feed quality, margins, and prepaid conversion goals.',
            },
            {
                'heading': 'The Result',
                'body': 'Consistent high-intent buyers at a profitable cost per order, layered on top of Meta for full-funnel coverage.',
            },
        ],
    },
    {
        'slug': 'factory-backoffice-ops',
        'title': 'Factory Backoffice That Runs Itself',
        'category': 'Operations',
        'client': 'Multi-SKU Garment Unit',
        'result': 'In-house team runs orders & support',
        'summary': 'SOPs, CRM, and staff training so D2C operations stay inside the factory.',
        'image': img('photo-1552664730-d307ca884978', 800, 600),
        'impact_areas': ['SOPs', 'CRM', 'Team Training'],
        'gallery': [
            img('photo-1552664730-d307ca884978', 1600, 900),
            img('photo-1553877522-43269d4ea984', 1600, 900),
            img('photo-1518186285589-2f7649de56e0', 1600, 900),
        ],
        'narrative': [
            {
                'heading': 'The Challenge',
                'body': 'Ads and store were working, but order chaos, returns, and support were burning the owner’s time.',
            },
            {
                'heading': 'The Approach',
                'body': 'We installed clear SOPs, a simple CRM/dashboard stack, and trained staff on orders, support, inventory, and returns.',
            },
            {
                'heading': 'The Result',
                'body': 'The in-house team now runs day-to-day D2C operations — the owner focuses on production and growth.',
            },
        ],
    },
]

INDUSTRIES = [
    {
        'title': 'Textile & Garment Manufacturers',
        'desc': 'Factory-to-customer pipelines for sarees, kurtis, t-shirts, jeans, and ethnic wear.',
        'icon': '🏭',
    },
    {
        'title': 'Factory Owners',
        'desc': 'Move from wholesale credit to prepaid D2C without losing control of production.',
        'icon': '🏗️',
    },
    {
        'title': 'Emerging D2C Brands',
        'desc': 'Store, ads, and ops systems for fashion brands selling direct online.',
        'icon': '🛍️',
    },
    {
        'title': 'Saree & Ethnic Wear',
        'desc': 'High-SKU catalogs, prepaid checkout, and Meta/Google demand generation.',
        'icon': '✨',
    },
    {
        'title': 'T-Shirt & Casual Wear',
        'desc': 'Volume-friendly storefronts and ads built for daily prepaid order flow.',
        'icon': '👕',
    },
    {
        'title': 'Visionary Entrepreneurs',
        'desc': 'Founders ready to own the customer relationship and brand equity.',
        'icon': '💡',
    },
]

PRICING_TIERS = [
    {
        'name': 'Starter',
        'price': '₹15,000',
        'price_monthly': '₹15,000',
        'price_annual': '₹13,500',
        'period': '/month',
        'features': [
            'Basic store setup',
            'Social media ads (1 platform)',
            'WhatsApp integration',
            'Monthly report',
        ],
        'highlight': False,
        'blurb': 'Perfect for small factories getting started with D2C.',
    },
    {
        'name': 'Growth',
        'price': '₹35,000',
        'price_monthly': '₹35,000',
        'price_annual': '₹31,500',
        'period': '/month',
        'features': [
            'Full store setup & optimization',
            'Meta + Google ads',
            'Email & WhatsApp automation',
            'Backoffice setup & training',
            'Weekly performance reports',
        ],
        'highlight': True,
        'blurb': 'For manufacturers ready to scale aggressively.',
    },
    {
        'name': 'Scale',
        'price': 'Custom',
        'price_monthly': 'Custom',
        'price_annual': 'Custom',
        'period': '',
        'features': [
            'Everything in Growth',
            'Dedicated account manager',
            'Multi-platform expansion',
            'Brand identity & creatives',
            'Priority support 24/7',
        ],
        'highlight': False,
        'blurb': 'Enterprise-grade for large factories with big ambitions.',
    },
]

PRICING_FAQS = [
    {
        'q': 'Can I switch plans later?',
        'a': 'Yes — upgrade or downgrade anytime; changes apply from your next billing cycle.',
    },
    {
        'q': 'Is there a setup fee?',
        'a': 'No separate setup fee on Starter or Growth. Scale plans may include scoped onboarding.',
    },
    {
        'q': 'What does annual billing save me?',
        'a': 'Annual billing is discounted roughly 10% compared to paying monthly.',
    },
    {
        'q': 'Do you customize for factory size?',
        'a': 'Yes — we tailor scope to your product category, SKU count, and growth goals.',
    },
    {
        'q': 'What is the minimum commitment?',
        'a': 'Month-to-month on Starter and Growth; Scale engagements are typically 6–12 months.',
    },
]

GENERAL_FAQS = [
    {
        'q': 'What is Winning Blueprints?',
        'a': (
            'Winning Blueprints is a D2C growth agency helping textile and garment manufacturers '
            'sell directly to customers online — eliminating wholesalers, distributors, and retailers '
            'to maximize profit margins. Behind the scenes, our Academy trains talent on real client work.'
        ),
    },
    {
        'q': 'How quickly can I start getting orders?',
        'a': (
            'Most clients start receiving prepaid orders within 30–45 days of onboarding. We set up '
            'your store, run first ad campaigns, and optimize for real buyer traffic as fast as possible.'
        ),
    },
    {
        'q': 'Do I need any technical knowledge?',
        'a': (
            'Not at all. We handle store setup, creatives, campaigns, and team training. You focus on '
            'production; we handle the digital side.'
        ),
    },
    {
        'q': 'What products do you specialize in?',
        'a': (
            'Textile and garment categories: sarees, kurtis, salwar suits, t-shirts, jeans, ethnic wear, '
            'and more. Our systems are built for high-SKU fashion inventory.'
        ),
    },
    {
        'q': 'How much can I increase my profit margins?',
        'a': (
            'By going direct-to-customer and removing 3–5 intermediary layers, most manufacturers see '
            'a 2x to 4x improvement in net margins. Exact numbers depend on your product and current model.'
        ),
    },
]

# Full Startup Plan — idea → income
STARTUP_PHASES = [
    {
        'num': '01',
        'slug': 'build',
        'short': 'Build',
        'title': 'Develop the App / Project',
        'subtitle': 'Turn the idea into a working product',
        'desc': (
            'We scope, design, and build your MVP or full product — web app, store, or custom system — '
            'with clean architecture, mobile-first UX, and launch-ready infrastructure.'
        ),
        'outcomes': [
            'Product roadmap & technical blueprint',
            'MVP or production build',
            'Admin / ops dashboards where needed',
            'Staging → production launch checklist',
        ],
        'duration': '4–10 weeks',
        'icon': '💻',
    },
    {
        'num': '02',
        'slug': 'team',
        'short': 'Team',
        'title': 'Help Create the Team',
        'subtitle': 'Right roles, right people, right structure',
        'desc': (
            'We define the org chart for your stage — founders, ops, marketing, support — and help you '
            'hire or assign the first operators so the business isn’t stuck on one person.'
        ),
        'outcomes': [
            'Role map & hiring scorecards',
            'Founding / early-team structure',
            'SOPs for who owns what',
            'Optional Academy talent pipeline',
        ],
        'duration': '2–4 weeks',
        'icon': '👥',
    },
    {
        'num': '03',
        'slug': 'train',
        'short': 'Train',
        'title': 'Train the Team',
        'subtitle': 'Make the team execution-ready',
        'desc': (
            'Hands-on training on tools, workflows, and daily rituals — so your people can run the product, '
            'orders, support, and campaigns without constant founder firefighting.'
        ),
        'outcomes': [
            'Tool & dashboard training',
            'Playbooks for daily / weekly ops',
            'QA checklists & escalation paths',
            'Shadow → solo handoff plan',
        ],
        'duration': '2–3 weeks',
        'icon': '🎓',
    },
    {
        'num': '04',
        'slug': 'plan',
        'short': 'Plan',
        'title': 'Plan Marketing & Operations',
        'subtitle': 'Strategy before spend',
        'desc': (
            'We build the go-to-market and ops plan: channels, offers, funnels, unit economics, inventory / '
            'fulfillment flow, and KPIs — so launch isn’t guesswork.'
        ),
        'outcomes': [
            'GTM & channel plan',
            'Offer & funnel design',
            'Ops & fulfillment blueprint',
            'Budget, KPIs & 90-day roadmap',
        ],
        'duration': '1–2 weeks',
        'icon': '📋',
    },
    {
        'num': '05',
        'slug': 'launch',
        'short': 'Launch',
        'title': 'Start Real Marketing & Operations',
        'subtitle': 'Idea → income',
        'desc': (
            'We go live: ads, content, WhatsApp / email, order handling, and weekly optimization — '
            'until you have real customers, prepaid revenue, and a team that can sustain growth.'
        ),
        'outcomes': [
            'Live campaigns & creatives',
            'Order / lead ops running',
            'Weekly performance reviews',
            'Path to repeatable revenue',
        ],
        'duration': 'Ongoing',
        'icon': '🚀',
    },
]

STARTUP_PROMISES = [
    {
        'title': 'One partner, full journey',
        'desc': 'Build → team → train → plan → launch under one roof. No handoff chaos between agencies.',
    },
    {
        'title': 'Product + people + growth',
        'desc': 'Most startups fail on ops and GTM, not code. We cover all three.',
    },
    {
        'title': 'Academy-backed delivery',
        'desc': 'Trained talent on real work — so you scale execution without bloating payroll overnight.',
    },
    {
        'title': 'Income as the finish line',
        'desc': 'We don’t stop at “shipped.” Success means customers, cash flow, and a runnable system.',
    },
]

STARTUP_FOR = [
    {'title': 'First-time founders', 'desc': 'You have the idea — we build the machine around it.'},
    {'title': 'Factory / D2C owners', 'desc': 'Going direct? We build store, team, and growth together.'},
    {'title': 'Operators with a product gap', 'desc': 'You can sell — we build the app and systems to scale.'},
    {'title': 'Teams stuck after MVP', 'desc': 'Shipped but no revenue? We fix GTM, ops, and execution.'},
]

STARTUP_FAQS = [
    {
        'q': 'Is this only for tech startups?',
        'a': (
            'No. It works for SaaS, D2C stores, service platforms, and manufacturer digital brands — '
            'anything that needs a product, a team, and a path to paying customers.'
        ),
    },
    {
        'q': 'Can I start from the middle (e.g. only marketing)?',
        'a': (
            'Yes. We diagnose where you are and plug into the right phase. The full plan is ideal when '
            'you’re starting from idea or rebuilding from scratch.'
        ),
    },
    {
        'q': 'How long until first revenue?',
        'a': (
            'Depends on product readiness. If the build is light, many clients see first paid traction '
            'within 30–60 days of the launch phase. Complex products take longer on Phase 1.'
        ),
    },
    {
        'q': 'Do you help hire or only train?',
        'a': (
            'Both. We help define roles and structure, support hiring decisions, and train whoever you '
            'bring — including talent from our Academy pipeline when it fits.'
        ),
    },
    {
        'q': 'What do you need from me to start?',
        'a': (
            'A clear problem you’re solving, who pays, and a decision-maker who can move weekly. '
            'We handle blueprint, build, team design, training, and go-to-market.'
        ),
    },
]

ACADEMY_PROCESS = [
    'Admission', 'Training', 'Assessment', 'Internal Internship',
    'Client Project', 'Portfolio', 'Placement',
]

OPEN_ROLES = [
    {
        'slug': 'meta-ads-specialist',
        'title': 'Meta Ads Specialist',
        'type': 'Full-time',
        'location': 'Surat / Hybrid',
        'dept': 'Marketing',
        'summary': 'Run Facebook & Instagram campaigns for manufacturer D2C brands — creative testing, audiences, and ROAS.',
        'tags': ['Meta Ads', 'Creative', 'ROAS'],
    },
    {
        'slug': 'google-ads-specialist',
        'title': 'Google Ads / Shopping Specialist',
        'type': 'Full-time',
        'location': 'Surat / Hybrid',
        'dept': 'Marketing',
        'summary': 'Own search and shopping campaigns for high-SKU fashion catalogs with prepaid conversion goals.',
        'tags': ['PPC', 'Shopping', 'Analytics'],
    },
    {
        'slug': 'fullstack-ecommerce',
        'title': 'Full-Stack / eCommerce Developer',
        'type': 'Full-time',
        'location': 'Surat / Remote',
        'dept': 'Tech',
        'summary': 'Build and ship storefronts, dashboards, and automation that power client D2C operations.',
        'tags': ['Django', 'Frontend', 'eCommerce'],
    },
    {
        'slug': 'ai-automation-engineer',
        'title': 'AI Automation Engineer',
        'type': 'Full-time',
        'location': 'Surat / Hybrid',
        'dept': 'Tech',
        'summary': 'Design AI agents and no-code/low-code workflows for marketing, sales, support, and ops.',
        'tags': ['AI', 'Automation', 'n8n'],
    },
    {
        'slug': 'ops-crm-associate',
        'title': 'Operations / CRM Associate',
        'type': 'Full-time',
        'location': 'Surat',
        'dept': 'Operations',
        'summary': 'SOPs, order workflows, WhatsApp support systems, and client backoffice training.',
        'tags': ['CRM', 'SOPs', 'CX'],
    },
    {
        'slug': 'growth-intern',
        'title': 'Growth Intern (Marketing / Ops / Dev)',
        'type': 'Internship',
        'location': 'Surat / Hybrid',
        'dept': 'Internship',
        'summary': 'Work on real client projects under seniors — portfolio, mentorship, and path to full-time.',
        'tags': ['Internship', 'Mentorship', 'Real projects'],
    },
]

CAREERS_PERKS = [
    {'title': 'Real client work', 'desc': 'No fake case studies — you ship on live manufacturer and startup accounts.'},
    {'title': 'Senior mentorship', 'desc': 'Learn under strategy, ads, tech, and ops leads — not sink-or-swim.'},
    {'title': 'Academy + delivery', 'desc': 'Train hard, then execute. Clear path from intern to specialist.'},
    {'title': 'Surat-rooted, India-wide', 'desc': 'Textile D2C heartland with remote-friendly roles where it fits.'},
]

STATS = [
    {'value': 12, 'suffix': '+', 'label': 'Years Experience'},
    {'value': 2, 'suffix': 'x', 'label': 'Profit Margins'},
    {'value': 98, 'suffix': '%', 'label': 'Satisfied Clients'},
    {'value': 3, 'suffix': 'X', 'label': 'Average ROI'},
]

CLIENT_LOGOS = [
    {'name': 'Textile', 'image': ''},
    {'name': 'Garment', 'image': ''},
    {'name': 'Saree', 'image': ''},
    {'name': 'T-Shirt', 'image': ''},
    {'name': 'Kurti', 'image': ''},
    {'name': 'D2C', 'image': ''},
    {'name': 'Factory', 'image': ''},
    {'name': 'Fashion', 'image': ''},
]

INSTAGRAM_IMAGES = [
    img('photo-1610030469983-98e550d6193c', 400, 400),
    img('photo-1523381210131-f77ef81b785a', 400, 400),
    img('photo-1483985988355-763728e1935b', 400, 400),
    img('photo-1441986300917-64674bd600d8', 400, 400),
    img('photo-1556742049-0cfed4f6a45d', 400, 400),
    img('photo-1611162616305-c69b3fa7fbe0', 400, 400),
    img('photo-1552664730-d307ca884978', 400, 400),
    img('photo-1518186285589-2f7649de56e0', 400, 400),
]

CONTACT_INFO = {
    'email': 'win@winningblueprints.com',
    'phone': '+91 90235 61533',
    'address': 'Adajan, Surat, Gujarat 395009',
    'hours': 'Mon–Fri, 9am–6pm IST',
}

TESTIMONIALS = [
    {
        'quote': (
            'Before Winning Blueprints, I was selling at wholesale rates and barely making 10% margin. '
            'Now I sell directly to my customers online, get prepaid orders every day, and my margins '
            'have gone up by 3x. This is the best decision I made for my factory.'
        ),
        'name': 'Ramesh Patel',
        'role': 'Saree Manufacturer',
        'company': 'Surat',
        'initials': 'RP',
        'photo': '',
    },
    {
        'quote': (
            'We were stuck in the traditional model — distributors, credit, delays. Winning Blueprints '
            'set up our store, ran our ads, and within 45 days we had daily orders flowing in. No credit, '
            'no middlemen, just pure profit straight to us.'
        ),
        'name': 'Priya Agarwal',
        'role': 'T-Shirt Factory Owner',
        'company': 'Tirupur',
        'initials': 'PA',
        'photo': '',
    },
    {
        'quote': (
            'They didn’t just run ads — they trained our team on orders and WhatsApp follow-ups. '
            'We finally own the customer relationship instead of depending on traders.'
        ),
        'name': 'Amit Shah',
        'role': 'Kurti Brand Founder',
        'company': 'Surat',
        'initials': 'AS',
        'photo': '',
    },
]
