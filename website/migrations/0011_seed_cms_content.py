"""Seed the new CMS tables (website.0010_cms_models) with exactly what
website/data.py already hardcodes, so the public site is byte-identical
before and after website/views.py is switched to read from these tables
instead of importing the data.py constants."""

from django.db import migrations


def _img(photo, w=1200, h=800):
    return f'https://images.unsplash.com/{photo}?auto=format&fit=crop&w={w}&h={h}&q=65'


TITLE_DESC_BLOCKS = [
    # section, title, desc, icon, image, badge
    ('why_choose_us', 'No More Credit Sales', 'Digital storefronts and prepaid systems so you get paid before dispatch — less risk, better cash flow.', '', '', ''),
    ('why_choose_us', 'Higher Profit Margins', 'Remove wholesalers and distributors. Earn what your product is worth — often 2x–4x more.', '', '', ''),
    ('why_choose_us', 'Tested Systems, Real Results', 'Field-tested with real factories. Store, ads, and ops systems built to scale.', '', '', ''),
    ('why_choose_us', 'Brand Control, Market Freedom', 'Own the customer, the data, and the experience. Stop depending on traders.', '', '', ''),

    ('startup_promises', 'One partner, full journey', 'Build → team → train → plan → launch under one roof. No handoff chaos between agencies.', '', '', ''),
    ('startup_promises', 'Product + people + growth', 'Most startups fail on ops and GTM, not code. We cover all three.', '', '', ''),
    ('startup_promises', 'Academy-backed delivery', 'Trained talent on real work — so you scale execution without bloating payroll overnight.', '', '', ''),
    ('startup_promises', 'Income as the finish line', 'We don’t stop at “shipped.” Success means customers, cash flow, and a runnable system.', '', '', ''),

    ('startup_for', 'First-time founders', 'You have the idea — we build the machine around it.', '', '', ''),
    ('startup_for', 'Factory / D2C owners', 'Going direct? We build store, team, and growth together.', '', '', ''),
    ('startup_for', 'Operators with a product gap', 'You can sell — we build the app and systems to scale.', '', '', ''),
    ('startup_for', 'Teams stuck after MVP', 'Shipped but no revenue? We fix GTM, ops, and execution.', '', '', ''),

    ('f2c_pipeline', 'Store Setup', 'Branded online store with mobile-first design, catalog, cart, and checkout.', '', '', ''),
    ('f2c_pipeline', 'Traffic & Ads', 'Meta & Google ads targeting real buyers — not vanity reach.', '', '', ''),
    ('f2c_pipeline', 'Prepaid Orders', 'Full payment before dispatch — zero credit risk, daily cash flow.', '', '', ''),
    ('f2c_pipeline', 'Scale & Profit', '2x–4x margins, repeat customers, and a brand you own.', '', '', ''),

    ('model_steps', 'D2C Growth Agency', 'What manufacturers hire — store setup, Meta & Google ads, prepaid order systems, and backoffice SOPs that take factories direct to customers.', '', _img('photo-1441986300917-64674bd600d8', 900, 600), ''),
    ('model_steps', 'Internal Academy', 'A talent development system that trains future specialists on real client work — not the headline clients see, but how we keep delivery sharp at scale.', '', _img('photo-1524178232363-1fb2b075b655', 900, 600), ''),
    ('model_steps', 'Better Delivery', 'Skilled teams, lower overhead, higher client satisfaction — the result of the agency + academy systems working together.', '', _img('photo-1600880292203-757bb62b4baf', 900, 600), ''),

    ('industries', 'Textile & Garment Manufacturers', 'Factory-to-customer pipelines for sarees, kurtis, t-shirts, jeans, and ethnic wear.', '🏭', '', ''),
    ('industries', 'Factory Owners', 'Move from wholesale credit to prepaid D2C without losing control of production.', '🏗️', '', ''),
    ('industries', 'Emerging D2C Brands', 'Store, ads, and ops systems for fashion brands selling direct online.', '🛍️', '', ''),
    ('industries', 'Saree & Ethnic Wear', 'High-SKU catalogs, prepaid checkout, and Meta/Google demand generation.', '✨', '', ''),
    ('industries', 'T-Shirt & Casual Wear', 'Volume-friendly storefronts and ads built for daily prepaid order flow.', '👕', '', ''),
    ('industries', 'Visionary Entrepreneurs', 'Founders ready to own the customer relationship and brand equity.', '💡', '', ''),

    ('team_departments', 'eCommerce Team', 'Store designers, developers, and catalog managers who build high-converting D2C storefronts.', '🛒', '', '25'),
    ('team_departments', 'Digital Marketing Team', 'Meta, Google, WhatsApp, and email specialists driving real buyers to your store every day.', '📣', '', '35'),
    ('team_departments', 'Operations Team', 'Backoffice trainers, SOP builders, and logistics coordinators keeping your D2C running smoothly.', '⚙️', '', '20'),
    ('team_departments', 'Analytics & Strategy', 'Data analysts and growth strategists constantly optimising campaigns, margins, and revenue.', '📊', '', '20'),

    ('team_roles', 'Strategy & Sales', '', '', _img('photo-1560250097-0b93528c311a', 200, 200), '4'),
    ('team_roles', 'Ads & SEO', '', '', _img('photo-1507003211169-0a1dd7228f2d', 200, 200), '6'),
    ('team_roles', 'Developers', '', '', _img('photo-1519085362263-aa42b02f1f9c', 200, 200), '8'),
    ('team_roles', 'Designers', '', '', _img('photo-1494790108377-be9c29b29330', 200, 200), '5'),
    ('team_roles', 'Ops & CRM', '', '', _img('photo-1500648767791-00dcc994a43e', 200, 200), '4'),

    ('careers_perks', 'Real client work', 'No fake case studies — you ship on live manufacturer and startup accounts.', '', '', ''),
    ('careers_perks', 'Senior mentorship', 'Learn under strategy, ads, tech, and ops leads — not sink-or-swim.', '', '', ''),
    ('careers_perks', 'Academy + delivery', 'Train hard, then execute. Clear path from intern to specialist.', '', '', ''),
    ('careers_perks', 'Surat-rooted, India-wide', 'Textile D2C heartland with remote-friendly roles where it fits.', '', '', ''),

    ('academy_process', 'Admission', '', '', '', ''),
    ('academy_process', 'Training', '', '', '', ''),
    ('academy_process', 'Assessment', '', '', '', ''),
    ('academy_process', 'Internal Internship', '', '', '', ''),
    ('academy_process', 'Client Project', '', '', '', ''),
    ('academy_process', 'Portfolio', '', '', '', ''),
    ('academy_process', 'Placement', '', '', '', ''),

    ('audience_tags', 'Textile Manufacturers', '', '', '', ''),
    ('audience_tags', 'Garment Factories', '', '', '', ''),
    ('audience_tags', 'Saree Brands', '', '', '', ''),
    ('audience_tags', 'T-Shirt Makers', '', '', '', ''),
    ('audience_tags', 'Kurti Producers', '', '', '', ''),
    ('audience_tags', 'D2C Fashion', '', '', '', ''),
    ('audience_tags', 'Factory Owners', '', '', '', ''),

    ('hero_points', 'Keep up to 60% more profit', '', '', '', ''),
    ('hero_points', 'Daily orders, full cash flow', '', '', '', ''),
    ('hero_points', 'Build a brand customers love', '', '', '', ''),
]

STAT_BLOCKS = [
    (12, '+', 'Years Experience'),
    (2, 'x', 'Profit Margins'),
    (98, '%', 'Satisfied Clients'),
    (3, 'X', 'Average ROI'),
]

PROJECT_BLOCKS = [
    ('Saree Brand D2C Store', 'eCommerce', 'Prepaid orders in 45 days', _img('photo-1610030469983-98e550d6193c', 800, 600)),
    ('T-Shirt Factory Meta Ads', 'Meta Ads', '3x margin vs wholesale', _img('photo-1523381210131-f77ef81b785a', 800, 600)),
    ('Kurti Brand Google Shopping', 'Google Ads', 'Daily high-intent buyers', _img('photo-1483985988355-763728e1935b', 800, 600)),
    ('Factory Backoffice SOPs', 'Operations', 'Team runs orders in-house', _img('photo-1552664730-d307ca884978', 800, 600)),
    ('WhatsApp Cart Recovery', 'Automation', '65% abandon recovery lift', _img('photo-1518186285589-2f7649de56e0', 800, 600)),
]

TESTIMONIALS = [
    (
        'Before Winning Blueprints, I was selling at wholesale rates and barely making 10% margin. '
        'Now I sell directly to my customers online, get prepaid orders every day, and my margins '
        'have gone up by 3x. This is the best decision I made for my factory.',
        'Ramesh Patel', 'Saree Manufacturer', 'Surat', 'RP', '',
    ),
    (
        'We were stuck in the traditional model — distributors, credit, delays. Winning Blueprints '
        'set up our store, ran our ads, and within 45 days we had daily orders flowing in. No credit, '
        'no middlemen, just pure profit straight to us.',
        'Priya Agarwal', 'T-Shirt Factory Owner', 'Tirupur', 'PA', '',
    ),
    (
        'They didn’t just run ads — they trained our team on orders and WhatsApp follow-ups. '
        'We finally own the customer relationship instead of depending on traders.',
        'Amit Shah', 'Kurti Brand Founder', 'Surat', 'AS', '',
    ),
]

FAQS = [
    # group, q, a
    ('pricing', 'Can I switch plans later?', 'Yes — upgrade or downgrade anytime; changes apply from your next billing cycle.'),
    ('pricing', 'Is there a setup fee?', 'No separate setup fee on Starter or Growth. Scale plans may include scoped onboarding.'),
    ('pricing', 'What does annual billing save me?', 'Annual billing is discounted roughly 10% compared to paying monthly.'),
    ('pricing', 'Do you customize for factory size?', 'Yes — we tailor scope to your product category, SKU count, and growth goals.'),
    ('pricing', 'What is the minimum commitment?', 'Month-to-month on Starter and Growth; Scale engagements are typically 6–12 months.'),

    ('general', 'What is Winning Blueprints?', 'Winning Blueprints is a D2C growth agency helping textile and garment manufacturers sell directly to customers online — eliminating wholesalers, distributors, and retailers to maximize profit margins. Behind the scenes, our Academy trains talent on real client work.'),
    ('general', 'How quickly can I start getting orders?', 'Most clients start receiving prepaid orders within 30–45 days of onboarding. We set up your store, run first ad campaigns, and optimize for real buyer traffic as fast as possible.'),
    ('general', 'Do I need any technical knowledge?', 'Not at all. We handle store setup, creatives, campaigns, and team training. You focus on production; we handle the digital side.'),
    ('general', 'What products do you specialize in?', 'Textile and garment categories: sarees, kurtis, salwar suits, t-shirts, jeans, ethnic wear, and more. Our systems are built for high-SKU fashion inventory.'),
    ('general', 'How much can I increase my profit margins?', 'By going direct-to-customer and removing 3–5 intermediary layers, most manufacturers see a 2x to 4x improvement in net margins. Exact numbers depend on your product and current model.'),

    ('startup', 'Is this only for tech startups?', 'No. It works for SaaS, D2C stores, service platforms, and manufacturer digital brands — anything that needs a product, a team, and a path to paying customers.'),
    ('startup', 'Can I start from the middle (e.g. only marketing)?', 'Yes. We diagnose where you are and plug into the right phase. The full plan is ideal when you’re starting from idea or rebuilding from scratch.'),
    ('startup', 'How long until first revenue?', 'Depends on product readiness. If the build is light, many clients see first paid traction within 30–60 days of the launch phase. Complex products take longer on Phase 1.'),
    ('startup', 'Do you help hire or only train?', 'Both. We help define roles and structure, support hiring decisions, and train whoever you bring — including talent from our Academy pipeline when it fits.'),
    ('startup', 'What do you need from me to start?', 'A clear problem you’re solving, who pays, and a decision-maker who can move weekly. We handle blueprint, build, team design, training, and go-to-market.'),

    ('lp_ai_dm', 'Is this suitable for beginners?', 'Yes. The program is designed as a beginner-friendly, practical introduction — most students join with zero prior experience.'),
    ('lp_ai_dm', 'Do I need coding experience?', 'No advanced coding experience is required for the Vibe Coding (AI-assisted development) module.'),
    ('lp_ai_dm', 'Is this completely online?', 'Yes. All 12 live training sessions are conducted online.'),
    ('lp_ai_dm', 'How many classes are there?', 'There are 12 live training days spread across 4 weeks — one week per skill: Vibe Coding, Meta Ads, Google Ads, and Client Handling.'),
    ('lp_ai_dm', 'Will I get practical assignments?', 'Yes. The program is built around learn → practice → build → apply, with a practical task after every module — not just video lectures.'),
    ('lp_ai_dm', 'Will you guarantee a job or clients?', "No. We don't make unrealistic guarantees. Your results depend on your own practice, execution, and ability to apply what you learn."),
    ('lp_ai_dm', 'Can I start freelancing after the course?', 'You can use the skills developed during the bootcamp as a foundation for freelancing. Getting clients still requires continued practice, portfolio development, outreach, and execution.'),
    ('lp_ai_dm', 'What do I need to join?', 'A laptop or desktop, an internet connection, and the willingness to practice.'),
]

TEAM_MEMBERS = [
    # name, role, tags, initials, bio, image, is_founder
    (
        'Singh Kriti', 'Operations Head & D2C Strategy Lead',
        ['D2C Strategy', 'Operations', 'Sales Systems'], 'SK',
        '12+ years in textile D2C strategy. Singh Kriti has personally guided 200+ manufacturers '
        'from wholesale dependency to profitable direct sales — building brands that customers love.',
        _img('photo-1573496359142-b8d87734a5a2', 480, 480), True,
    ),
    (
        'Kr. Sunil Verma', 'Founder & CEO',
        ['AI Automation Engineer', 'Tech Architecture', 'eCommerce'], 'KSV',
        'Founder & CEO and AI Automation Engineer with a decade of eCommerce experience. '
        'Sunil architects the digital infrastructure and AI automation that powers every client’s '
        'D2C operation — from store to analytics.',
        _img('photo-1472099645785-5658abf4ff4e', 480, 480), True,
    ),
    ('ShreeVastav Mayank', 'Marketing Expert', ['Meta Ads', 'SEO'], 'SM',
     'Runs Meta and organic programs that bring real buyers — not empty traffic.',
     _img('photo-1507003211169-0a1dd7228f2d', 400, 400), False),
    ('Dutta Anubhav', 'Operations Head', ['Ops', 'CRM'], 'DA',
     'SOPs, CRM, and backoffice workflows so your team can run D2C day-to-day.',
     _img('photo-1500648767791-00dcc994a43e', 400, 400), False),
    ('Neha Rawat', 'Creative Director', ['Design', 'Brand'], 'NR',
     'Brand systems and creatives that make factory products feel like consumer brands.',
     _img('photo-1494790108377-be9c29b29330', 400, 400), False),
    ('Arjun Kaushik', 'Google Ads Lead', ['PPC', 'Shopping'], 'AK',
     'High-intent search and shopping campaigns for ready-to-buy customers.',
     _img('photo-1519085362263-aa42b02f1f9c', 400, 400), False),
    ('Priya Sharma', 'Content Strategist', ['Content', 'Email'], 'PS',
     'Product stories, email sequences, and catalog copy that convert browsers into buyers.',
     _img('photo-1580489944761-15a19d654956', 400, 400), False),
    ('Ravi Verma', 'Logistics Manager', ['Logistics', '3PL'], 'RV',
     'Dispatch, 3PL, and fulfillment workflows that keep prepaid orders moving on time.',
     _img('photo-1560250097-0b93528c311a', 400, 400), False),
    ('Sneha Gupta', 'Customer Success', ['Support', 'CX'], 'SG',
     'Post-purchase support and CX systems that turn first orders into repeat buyers.',
     _img('photo-1438761681033-6461ffad8d80', 400, 400), False),
    ('Mohit Jain', 'Analytics Lead', ['Data', 'ROI'], 'MJ',
     'Dashboards and ROI tracking so every rupee of ad spend is accountable.',
     _img('photo-1506794778202-cad84cf45f1d', 400, 400), False),
]

SERVICES = [
    # slug, title, icon, short, description, gallery, is_flagship, flagship_features, popular
    (
        'website-development', 'eCommerce & Website', '💻',
        'Branded online stores built for textile catalogs and prepaid checkout.',
        'We build mobile-first storefronts with product pages, categories, cart, and checkout — '
        'ready for sarees, kurtis, t-shirts, jeans, and high-SKU fashion inventory. Supports both '
        'direct-to-customer (B2C) and bulk/wholesale (B2B) orders.',
        [_img('photo-1467232004584-a241de8bcf5d', 1200, 800), _img('photo-1556742049-0cfed4f6a45d', 1200, 800)],
        True, ['Tailored storefront', 'Full catalog control', 'Mobile-first, sales-ready'], False,
    ),
    (
        'meta-ads', 'Meta Ads', '📱',
        'Facebook & Instagram ads that generate daily prepaid orders for factories.',
        'Creative-first Meta campaigns using interests, behavior, and lookalike audiences — '
        'built to get real buyers for sarees, kurtis, t-shirts, and garment brands.',
        [_img('photo-1611162616305-c69b3fa7fbe0', 1200, 800), _img('photo-1563986768609-322da13575f3', 1200, 800)],
        True, ['Meta & Google ads setup', 'WhatsApp + email automation', 'Performance tracking & ROI'], True,
    ),
    (
        'google-ads', 'Google Ads', '📈',
        'High-intent search and shopping ads for ready-to-buy customers.',
        'We set up search and shopping campaigns that capture customers already looking for '
        'your products — focused on prepaid conversions and measurable ROI.',
        [_img('photo-1556761175-b1176c4bbf9b', 1200, 800), _img('photo-1460925895917-afdab827c52f', 1200, 800)],
        False, [], False,
    ),
    (
        'seo', 'SEO', '🔍',
        'Organic visibility so buyers find your brand without paid spend alone.',
        'Technical SEO, product/category content, and authority building tailored for '
        'fashion and textile D2C brands that need lasting organic demand.',
        [_img('photo-1432888498266-38ff6183fd6a', 1200, 800), _img('photo-1551288049-bebda4e38f71', 1200, 800)],
        False, [], False,
    ),
    (
        'automation', 'WhatsApp & Automation', '⚡',
        'Cart recovery, order updates, and lead flows on WhatsApp & email.',
        'We connect your store, ads, and messaging tools so abandoned carts recover, '
        'orders update automatically, and your team spends less time on manual follow-ups.',
        [_img('photo-1518186285589-2f7649de56e0', 1200, 800), _img('photo-1485827404703-89b55fcc595e', 1200, 800)],
        False, [], False,
    ),
    (
        'crm', 'Backoffice & CRM', '🗂️',
        'SOPs, dashboards, and CRM so your factory runs D2C like a machine.',
        'Order management, customer support workflows, inventory visibility, and CRM setup — '
        'plus training so your staff can run day-to-day operations without us in the room.',
        [_img('photo-1552664730-d307ca884978', 1200, 800), _img('photo-1553877522-43269d4ea984', 1200, 800)],
        True, ['Team training & SOPs', 'Tool & dashboard setup', 'Daily operations setup'], False,
    ),
    (
        'branding', 'Brand Identity', '🎨',
        'A brand customers trust — so you stop depending on traders.',
        'Logo, visual identity, messaging, and creatives that position your factory as a '
        'direct-to-customer brand customers remember and reorder from.',
        [_img('photo-1561070791-2526d30994b5', 1200, 800), _img('photo-1626785774573-4b799315345d', 1200, 800)],
        False, [], False,
    ),
    (
        'content-marketing', 'Content Marketing', '✍️',
        'Product stories and social content that educate and convert buyers.',
        'Catalog copy, social creatives, email sequences, and product storytelling crafted '
        'for textile and garment brands selling direct online.',
        [_img('photo-1455390582261-044cdead277a', 1200, 800), _img('photo-1504868584819-f8e8b4b6d7e3', 1200, 800)],
        False, [], False,
    ),
]

CASE_STUDIES = [
    (
        'saree-manufacturer-d2c', 'From 10% Margins to 3x Profit', 'D2C Transformation',
        'Saree Manufacturer, Surat', '3x margins with daily prepaid orders',
        'Moved a Surat saree manufacturer from wholesale credit sales to a branded D2C store '
        'with Meta ads and prepaid checkout.',
        _img('photo-1610030469983-98e550d6193c', 800, 600),
        ['Profit Margins', 'Prepaid Orders', 'Brand Ownership'],
        [
            _img('photo-1610030469983-98e550d6193c', 1600, 900),
            _img('photo-1556742049-0cfed4f6a45d', 1600, 900),
            _img('photo-1441986300917-64674bd600d8', 1600, 900),
        ],
        [
            {'heading': 'The Challenge', 'body': 'Wholesale rates left barely 10% margin. Credit sales, distributors, and delays controlled cash flow — the factory owned production but not the customer.'},
            {'heading': 'The Approach', 'body': 'We launched a branded store, ran Meta ads to real buyers, and set up prepaid checkout plus WhatsApp order workflows so payment came before dispatch.'},
            {'heading': 'The Result', 'body': 'Margins rose ~3x. Daily prepaid orders replaced credit risk. The manufacturer now owns the brand, the data, and the relationship with end customers.'},
        ],
    ),
    (
        'tshirt-factory-meta-ads', 'T-Shirt Factory: Orders in 45 Days', 'Meta Ads',
        'T-Shirt Factory, Tirupur', 'Daily prepaid orders within 45 days',
        'Store setup + Meta ads took a Tirupur t-shirt factory from distributor dependency '
        'to daily prepaid D2C orders.',
        _img('photo-1523381210131-f77ef81b785a', 800, 600),
        ['Time to Orders', 'Cash Flow', 'No Middlemen'],
        [
            _img('photo-1523381210131-f77ef81b785a', 1600, 900),
            _img('photo-1611162616305-c69b3fa7fbe0', 1600, 900),
            _img('photo-1563986768609-322da13575f3', 1600, 900),
        ],
        [
            {'heading': 'The Challenge', 'body': 'Stuck in the traditional model — distributors, credit, and delays. No direct path to end customers or predictable prepaid revenue.'},
            {'heading': 'The Approach', 'body': 'We set up the store, launched Facebook & Instagram campaigns, and trained the team on order handling so fulfillment stayed inside the factory.'},
            {'heading': 'The Result', 'body': 'Within 45 days, daily prepaid orders were flowing. No credit, no middlemen — profit straight to the factory.'},
        ],
    ),
    (
        'kurti-brand-google-shopping', 'Kurti Brand Google Shopping Scale', 'Google Ads',
        'Ethnic Wear Brand', 'High-intent buyers at profitable CPL',
        'Shopping and search ads capturing ready-to-buy customers for ethnic wear SKUs.',
        _img('photo-1483985988355-763728e1935b', 800, 600),
        ['Shopping Ads', 'Intent Traffic', 'Catalog Scale'],
        [
            _img('photo-1483985988355-763728e1935b', 1600, 900),
            _img('photo-1460925895917-afdab827c52f', 1600, 900),
            _img('photo-1556761175-b1176c4bbf9b', 1600, 900),
        ],
        [
            {'heading': 'The Challenge', 'body': 'Meta alone was not enough — high-intent search demand for kurtis and ethnic wear was going to competitors.'},
            {'heading': 'The Approach', 'body': 'We structured Google Shopping and search campaigns around catalog feed quality, margins, and prepaid conversion goals.'},
            {'heading': 'The Result', 'body': 'Consistent high-intent buyers at a profitable cost per order, layered on top of Meta for full-funnel coverage.'},
        ],
    ),
    (
        'factory-backoffice-ops', 'Factory Backoffice That Runs Itself', 'Operations',
        'Multi-SKU Garment Unit', 'In-house team runs orders & support',
        'SOPs, CRM, and staff training so D2C operations stay inside the factory.',
        _img('photo-1552664730-d307ca884978', 800, 600),
        ['SOPs', 'CRM', 'Team Training'],
        [
            _img('photo-1552664730-d307ca884978', 1600, 900),
            _img('photo-1553877522-43269d4ea984', 1600, 900),
            _img('photo-1518186285589-2f7649de56e0', 1600, 900),
        ],
        [
            {'heading': 'The Challenge', 'body': 'Ads and store were working, but order chaos, returns, and support were burning the owner’s time.'},
            {'heading': 'The Approach', 'body': 'We installed clear SOPs, a simple CRM/dashboard stack, and trained staff on orders, support, inventory, and returns.'},
            {'heading': 'The Result', 'body': 'The in-house team now runs day-to-day D2C operations — the owner focuses on production and growth.'},
        ],
    ),
]

PRICING_TIERS = [
    (
        'Starter', '₹15,000', '₹15,000', '₹13,500', '/month',
        ['Basic store setup', 'Social media ads (1 platform)', 'WhatsApp integration', 'Monthly report'],
        False, 'Perfect for small factories getting started with D2C.',
    ),
    (
        'Growth', '₹35,000', '₹35,000', '₹31,500', '/month',
        ['Full store setup & optimization', 'Meta + Google ads', 'Email & WhatsApp automation', 'Backoffice setup & training', 'Weekly performance reports'],
        True, 'For manufacturers ready to scale aggressively.',
    ),
    (
        'Scale', 'Custom', 'Custom', 'Custom', '',
        ['Everything in Growth', 'Dedicated account manager', 'Multi-platform expansion', 'Brand identity & creatives', 'Priority support 24/7'],
        False, 'Enterprise-grade for large factories with big ambitions.',
    ),
]

STARTUP_PHASES = [
    (
        '01', 'build', 'Build', 'Develop the App / Project', 'Turn the idea into a working product',
        'We scope, design, and build your MVP or full product — web app, store, or custom system — '
        'with clean architecture, mobile-first UX, and launch-ready infrastructure.',
        ['Product roadmap & technical blueprint', 'MVP or production build', 'Admin / ops dashboards where needed', 'Staging → production launch checklist'],
        '4–10 weeks', '💻',
    ),
    (
        '02', 'team', 'Team', 'Help Create the Team', 'Right roles, right people, right structure',
        'We define the org chart for your stage — founders, ops, marketing, support — and help you '
        'hire or assign the first operators so the business isn’t stuck on one person.',
        ['Role map & hiring scorecards', 'Founding / early-team structure', 'SOPs for who owns what', 'Optional Academy talent pipeline'],
        '2–4 weeks', '👥',
    ),
    (
        '03', 'train', 'Train', 'Train the Team', 'Make the team execution-ready',
        'Hands-on training on tools, workflows, and daily rituals — so your people can run the product, '
        'orders, support, and campaigns without constant founder firefighting.',
        ['Tool & dashboard training', 'Playbooks for daily / weekly ops', 'QA checklists & escalation paths', 'Shadow → solo handoff plan'],
        '2–3 weeks', '🎓',
    ),
    (
        '04', 'plan', 'Plan', 'Plan Marketing & Operations', 'Strategy before spend',
        'We build the go-to-market and ops plan: channels, offers, funnels, unit economics, inventory / '
        'fulfillment flow, and KPIs — so launch isn’t guesswork.',
        ['GTM & channel plan', 'Offer & funnel design', 'Ops & fulfillment blueprint', 'Budget, KPIs & 90-day roadmap'],
        '1–2 weeks', '📋',
    ),
    (
        '05', 'launch', 'Launch', 'Start Real Marketing & Operations', 'Idea → income',
        'We go live: ads, content, WhatsApp / email, order handling, and weekly optimization — '
        'until you have real customers, prepaid revenue, and a team that can sustain growth.',
        ['Live campaigns & creatives', 'Order / lead ops running', 'Weekly performance reviews', 'Path to repeatable revenue'],
        'Ongoing', '🚀',
    ),
]

SITE_SETTINGS = {
    'hero_image': _img('photo-1558769132-cb1aea458c5e', 640, 420),
    'contact_bg_image': _img('photo-1441986300917-64674bd600d8', 1400, 700),
    'about_team_image': _img('photo-1556761175-5973dc0f32e7', 800, 600),
    'contact_email': 'winningblueprints@gmail.com',
    'contact_phone': '090235 61533',
    'contact_address': 'Adajan Gam, Adajan, Surat, Gujarat 395009',
    'contact_hours': 'Mon–Fri, 9am–6pm IST',
}


def seed_cms_content(apps, schema_editor):
    TitleDescBlock = apps.get_model('website', 'TitleDescBlock')
    StatBlock = apps.get_model('website', 'StatBlock')
    ProjectBlock = apps.get_model('website', 'ProjectBlock')
    Testimonial = apps.get_model('website', 'Testimonial')
    FAQ = apps.get_model('website', 'FAQ')
    TeamMember = apps.get_model('website', 'TeamMember')
    Service = apps.get_model('website', 'Service')
    CaseStudy = apps.get_model('website', 'CaseStudy')
    PricingTier = apps.get_model('website', 'PricingTier')
    StartupPhase = apps.get_model('website', 'StartupPhase')
    SiteSettings = apps.get_model('website', 'SiteSettings')

    for order, (section, title, desc, icon, image, badge) in enumerate(TITLE_DESC_BLOCKS):
        TitleDescBlock.objects.get_or_create(
            section=section, title=title,
            defaults={'desc': desc, 'icon': icon, 'image': image, 'badge': badge, 'order': order},
        )

    for order, (value, suffix, label) in enumerate(STAT_BLOCKS):
        StatBlock.objects.get_or_create(label=label, defaults={'value': value, 'suffix': suffix, 'order': order})

    for order, (title, category, result, image) in enumerate(PROJECT_BLOCKS):
        ProjectBlock.objects.get_or_create(
            title=title, defaults={'category': category, 'result': result, 'image': image, 'order': order},
        )

    for order, (quote, name, role, company, initials, photo) in enumerate(TESTIMONIALS):
        Testimonial.objects.get_or_create(
            name=name, role=role,
            defaults={'quote': quote, 'company': company, 'initials': initials, 'photo': photo, 'order': order},
        )

    group_orders = {}
    for group, question, answer in FAQS:
        order = group_orders.get(group, 0)
        group_orders[group] = order + 1
        FAQ.objects.get_or_create(group=group, question=question, defaults={'answer': answer, 'order': order})

    for order, (name, role, tags, initials, bio, image, is_founder) in enumerate(TEAM_MEMBERS):
        TeamMember.objects.get_or_create(
            name=name, role=role,
            defaults={'tags': tags, 'initials': initials, 'bio': bio, 'image': image, 'is_founder': is_founder, 'order': order},
        )

    for order, (slug, title, icon, short, description, gallery, is_flagship, flagship_features, popular) in enumerate(SERVICES):
        Service.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title, 'icon': icon, 'short': short, 'description': description,
                'gallery': gallery, 'is_flagship': is_flagship, 'flagship_features': flagship_features,
                'popular': popular, 'order': order,
            },
        )

    for order, (slug, title, category, client, result, summary, image, impact_areas, gallery, narrative) in enumerate(CASE_STUDIES):
        CaseStudy.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title, 'category': category, 'client': client, 'result': result,
                'summary': summary, 'image': image, 'impact_areas': impact_areas,
                'gallery': gallery, 'narrative': narrative, 'order': order,
            },
        )

    for order, (name, price, price_monthly, price_annual, period, features, highlight, blurb) in enumerate(PRICING_TIERS):
        PricingTier.objects.get_or_create(
            name=name,
            defaults={
                'price': price, 'price_monthly': price_monthly, 'price_annual': price_annual,
                'period': period, 'features': features, 'highlight': highlight, 'blurb': blurb, 'order': order,
            },
        )

    for order, (num, slug, short, title, subtitle, desc, outcomes, duration, icon) in enumerate(STARTUP_PHASES):
        StartupPhase.objects.get_or_create(
            slug=slug,
            defaults={
                'num': num, 'short': short, 'title': title, 'subtitle': subtitle, 'desc': desc,
                'outcomes': outcomes, 'duration': duration, 'icon': icon, 'order': order,
            },
        )

    SiteSettings.objects.get_or_create(pk=1, defaults=SITE_SETTINGS)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_cms_models'),
    ]

    operations = [
        migrations.RunPython(seed_cms_content, noop),
    ]
