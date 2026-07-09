"""Public academy course catalog — structured content for course pages."""

from website.data import img


def _mod(title, topics, free_preview=False):
    return {'title': title, 'topics': topics, 'free_preview': free_preview}


COURSES = [
    {
        'slug': 'ai-automation-engineering',
        'title': 'AI Automation Engineering Pro',
        'goal': (
            'Become a practical AI Automation Engineer who can build AI-powered business '
            'automation systems, create AI agents and workflows, and automate marketing, '
            'sales, support, and operations using no-code and low-code tools.'
        ),
        'level': 'Intermediate',
        'duration': '12 weeks',
        'format': 'Self-paced',
        'modules_count': 12,
        'topics_count': 84,
        'price': '₹16,999',
        'salary_range': '₹4–12 LPA',
        'featured': True,
        'enrolled': 83,
        'rating': 5.0,
        'reviews_count': 3,
        'image': img('photo-1677442136019-21780ecad995', 800, 500),
        'gains': [
            'Build production-ready AI automation workflows for business and client use',
            'Create portfolio-ready AI agents and automation projects for freelancing or jobs',
            'Earn a verified Winning Blueprints certificate and practical implementation experience',
        ],
        'includes': [
            '12 weeks of on-demand video content',
            'Completion certificate',
            'Hands-on projects & capstone implementation',
            'Live mentor Q&A support',
            'Mobile & desktop access',
            'Lifetime access',
        ],
        'learn_modules': [
            'AI Automation Foundations', 'Prompt Engineering & LLM Basics', 'API Integration Essentials',
            'Workflow Automation Tools', 'AI Agent Development', 'Database & Data Automation',
            'Business Automation Systems', 'AI Content Automation', 'Deployment & Production Systems',
            'Client Projects & Freelancing', 'Advanced AI Automation', 'Capstone & Career Launch',
        ],
        'ideal_paths': [
            'AI Automation Engineer', 'Workflow Automation Specialist', 'AI Implementation Consultant',
            'No-Code Automation Developer', 'Automation Freelancer', 'AI Operations Associate',
            'Business Process Automation Analyst',
        ],
        'overview': [
            'Master practical AI automation engineering with a business-first, deployment-focused learning approach built for intermediate learners, professionals, freelancers, and tech builders.',
            'Build in-demand skills including AI workflows, prompt engineering, API integrations, webhooks, AI agents, data automation, and business process automation.',
            'Work on real-world use cases like lead generation, CRM automation, AI support systems, content pipelines, reporting automation, and client delivery workflows.',
            'Get structured video lessons, practical assignments, mentor support, downloadable resources, lifetime access, and hands-on portfolio-ready capstone projects.',
            'Prepare for India-focused job roles, freelance automation consulting, startup implementation opportunities, and high-growth AI automation careers.',
        ],
        'curriculum': [
            _mod('AI Automation Foundations', [
                'Introduction to AI automation engineering', 'AI automation use cases in business',
                'Understanding workflows and process mapping', 'Automation thinking framework',
                'AI tools ecosystem overview', 'Assignment: business workflow analysis',
                'Automation opportunity identification',
            ], True),
            _mod('Prompt Engineering & LLM Basics', [
                'How LLMs work', 'Prompt engineering fundamentals', 'System prompts vs user prompts',
                'Prompt chaining techniques', 'Structured output prompting', 'Prompt debugging methods',
                'Assignment: AI prompt workflows',
            ], True),
            _mod('API Integration Essentials', [
                'What APIs are', 'REST API fundamentals', 'Authentication methods',
                'API requests and responses', 'JSON handling basics', 'Webhook concepts',
                'Assignment: connect external APIs',
            ]),
            _mod('Workflow Automation Tools', [
                'Automation platform fundamentals', 'Trigger and action design', 'Conditional logic workflows',
                'Data transformation concepts', 'Error handling strategies', 'Workflow optimization',
                'Assignment: business automation workflow',
            ]),
            _mod('AI Agent Development', [
                'AI agent fundamentals', 'Agent decision-making flows', 'Memory concepts',
                'Tool calling basics', 'Multi-step automation agents', 'Task delegation workflows',
                'Assignment: simple AI agent',
            ]),
            _mod('Database & Data Automation', [
                'Database fundamentals', 'Structured data handling', 'Spreadsheet automation',
                'CRM automation basics', 'Data cleaning workflows', 'Data sync automation',
                'Assignment: automated data pipeline',
            ]),
            _mod('Business Automation Systems', [
                'Sales automation workflows', 'Lead capture automation', 'Email automation systems',
                'Customer support automation', 'Invoice and reporting automation', 'Operations automation',
                'Assignment: automate a business process',
            ]),
            _mod('AI Content Automation', [
                'Content workflow automation', 'AI copy generation systems', 'SEO automation basics',
                'Social media workflow automation', 'Media processing automation', 'Publishing pipelines',
                'Assignment: content automation engine',
            ]),
            _mod('Deployment & Production Systems', [
                'Deployment fundamentals', 'Cloud hosting basics', 'Environment management',
                'Secrets and API key management', 'Monitoring workflows', 'Production troubleshooting',
                'Assignment: deploy automation workflow',
            ]),
            _mod('Client Projects & Freelancing', [
                'Automation project discovery', 'Client requirement gathering', 'Proposal writing basics',
                'Pricing automation services', 'Freelance delivery workflows', 'Client communication systems',
                'Assignment: mock client automation project',
            ]),
            _mod('Advanced AI Automation', [
                'Multi-agent workflows', 'Advanced decision automation', 'AI workflow orchestration',
                'Scalable architecture concepts', 'Performance optimization', 'Advanced troubleshooting',
                'Assignment: enterprise workflow design',
            ]),
            _mod('Capstone & Career Launch', [
                'Capstone project planning', 'Portfolio creation', 'Resume optimization for AI roles',
                'Interview preparation', 'Freelancing launch strategy', 'Final project presentation',
                'Career roadmap planning',
            ]),
        ],
        'career': {'min': '₹4L', 'max': '₹12L', 'label': 'Entry to senior roles'},
        'reviews': [
            {'quote': 'The practical workflows helped me start offering automation services to small businesses. I recovered the course fee through freelance work within two months.', 'name': 'Rahul Mehta', 'role': 'Automation Freelancer', 'city': 'Pune'},
            {'quote': 'I moved from repetitive manual work to building automation systems for my team. The modules were practical and easy to implement in real business scenarios.', 'name': 'Priya Sharma', 'role': 'Operations Executive', 'city': 'Bengaluru'},
            {'quote': 'The agent-building and API integration modules gave me confidence for interviews. The capstone project became a strong portfolio asset.', 'name': 'Amit Verma', 'role': 'Implementation Associate', 'city': 'Ahmedabad'},
        ],
        'highlight_quote': 'The practical workflows helped me start offering automation services to small businesses.',
        'highlight_author': 'Rahul Mehta, Automation Freelancer',
        'starts_with': 'AI Automation Foundations',
    },
    {
        'slug': 'ai-startup-pro-program',
        'title': 'AI Startup Pro Program',
        'goal': (
            'Learn digital marketing, website design, office productivity, sales communication, '
            'and mobile app development with AI. Become job-ready, freelancing-ready, or launch '
            'your own digital business in just 12 weeks.'
        ),
        'level': 'Intermediate',
        'duration': '12 weeks',
        'format': 'Self-paced',
        'modules_count': 12,
        'topics_count': 84,
        'price': '₹24,999',
        'salary_range': '₹3–12 LPA',
        'featured': True,
        'enrolled': 83,
        'rating': 5.0,
        'reviews_count': 3,
        'image': img('photo-1556761175-5973dc0f32e7', 800, 500),
        'gains': [
            'Run Meta Ads, Google Ads, SEO campaigns, and Canva design projects for businesses',
            'Build real websites and AI-powered mobile apps with practical project experience',
            'Become job-ready, freelancing-ready, or startup-ready with hands-on implementation skills',
        ],
        'includes': [
            '12 weeks of on-demand practical training', 'Completion certificate',
            'Digital marketing live projects', 'Website design project',
            'Mobile app development capstone', 'Office productivity & communication training',
            'Live mentor support', 'Lifetime access',
        ],
        'learn_modules': [
            'Digital Marketing Foundations + Canva', 'Meta Ads Mastery', 'Google Ads Mastery',
            'SEO Mastery', 'AI Website Design Fundamentals', 'Real Website Development',
            'Office Productivity Skills', 'Communication + Sales Skills',
            'Mobile App Development Foundations', 'AI App Building', 'Real Mobile App Project',
            'Deployment + Career Launch',
        ],
        'ideal_paths': [
            'Digital Marketing Executive', 'Performance Marketer', 'SEO Executive',
            'Website Designer', 'Social Media Manager', 'App Development Associate',
        ],
        'overview': [
            'Complete 12-week digital career transformation program designed for students, job seekers, freelancers, and aspiring entrepreneurs.',
            'Focused on practical implementation — Meta Ads, Google Ads, SEO, Canva, website design, office productivity, sales communication, and AI app building.',
            'Real projects include social media ad campaigns, SEO optimization, business website build, portfolio website, and mobile app project.',
            'Career outcomes: Digital Marketing Executive, SEO Executive, Performance Marketer, Website Designer, Freelancer, or startup founder pathway.',
            'Final capstone: build a real website, launch a working app prototype, create a portfolio, and prepare for jobs, freelancing, or business.',
        ],
        'curriculum': [
            _mod('Digital Marketing Foundations + Canva', [
                'Digital marketing introduction', 'Business branding fundamentals', 'Customer psychology',
                'Canva design basics', 'Social media creatives', 'AI content creation tools',
                'Assignment: social media design project',
            ], True),
            _mod('Meta Ads Mastery', [
                'Facebook Ads setup', 'Instagram Ads setup', 'Business Manager', 'Campaign objectives',
                'Audience targeting', 'Lead generation ads', 'Retargeting basics',
            ], True),
            _mod('Google Ads Mastery', [
                'Google Ads account setup', 'Search campaigns', 'Display campaigns', 'Keyword research',
                'Ad copywriting with AI', 'Conversion tracking', 'Lead generation campaigns',
            ]),
            _mod('SEO Mastery', [
                'SEO fundamentals', 'On-page SEO', 'Technical SEO basics', 'Local SEO',
                'Keyword research', 'SEO audit basics', 'Assignment: SEO optimization project',
            ]),
            _mod('AI Website Design Fundamentals', [
                'Domain & hosting basics', 'Website planning', 'UI/UX basics', 'AI website builders',
                'Landing page design', 'Canva website assets', 'Business website structure',
            ]),
            _mod('Real Website Development', [
                'Business website creation', 'Portfolio website', 'Contact forms', 'WhatsApp integration',
                'Payment integration basics', 'SEO setup', 'Website deployment',
            ]),
            _mod('Office Productivity Skills', [
                'MS Word', 'MS Excel', 'PowerPoint', 'Google Workspace', 'Professional documentation',
                'Business email writing', 'Office productivity workflows',
            ]),
            _mod('Communication + Sales Skills', [
                'English communication basics', 'Client communication', 'Sales psychology',
                'Telecalling skills', 'Proposal writing', 'Interview preparation', 'Business communication',
            ]),
            _mod('Mobile App Development Foundations', [
                'Mobile app ecosystem', 'UI/UX basics', 'AI coding tools', 'Prompt engineering',
                'App planning', 'Wireframing', 'Development workflow',
            ]),
            _mod('AI App Building', [
                'No-code app builders', 'FlutterFlow basics', 'Authentication', 'Database basics',
                'API basics', 'App workflows', 'Testing basics',
            ]),
            _mod('Real Mobile App Project', [
                'CRUD operations', 'Forms handling', 'Notifications', 'Payment integration',
                'Testing', 'Debugging', 'Project build',
            ]),
            _mod('Deployment + Career Launch', [
                'APK build', 'Play Store publishing basics', 'Portfolio creation', 'Freelancing roadmap',
                'Job interview preparation', 'Startup mindset', 'Final capstone project',
            ]),
        ],
        'career': {'min': '₹3L', 'max': '₹12L', 'label': 'Entry to senior roles'},
        'reviews': [
            {'quote': 'This course gave me practical Meta Ads, SEO, and Google Ads skills with real projects. I became job-ready within months.', 'name': 'Rahul Mehta', 'role': 'Digital Marketing Executive', 'city': 'Ahmedabad'},
            {'quote': 'Website design and Canva training helped me start freelancing quickly. The AI tools made learning much faster.', 'name': 'Pooja Sharma', 'role': 'Freelancer', 'city': 'Surat'},
            {'quote': 'The mobile app module made app development simple with AI tools. Great beginner-friendly practical training.', 'name': 'Amit Verma', 'role': 'App Development Learner', 'city': 'Delhi'},
        ],
        'highlight_quote': 'This course gave me practical Meta Ads, SEO, and Google Ads skills with real projects.',
        'highlight_author': 'Rahul Mehta, Digital Marketing Executive',
        'starts_with': 'Digital Marketing Foundations + Canva',
    },
    {
        'slug': 'ai-for-business-owners-mastery',
        'title': 'AI for Business Owners Mastery',
        'goal': (
            'Learn practical AI tools, automation, marketing, and business growth systems to scale faster — '
            'built for entrepreneurs, business owners, and aspiring AI implementation professionals.'
        ),
        'level': 'Beginner',
        'duration': '8 weeks',
        'format': 'Self-paced',
        'modules_count': 8,
        'topics_count': 56,
        'price': '₹18,999',
        'salary_range': '₹3–12 LPA',
        'featured': True,
        'enrolled': 83,
        'rating': 5.0,
        'reviews_count': 3,
        'image': img('photo-1553877522-43269d4ea984', 800, 500),
        'gains': [
            'Build AI-powered business workflows to automate operations, sales, and customer communication',
            'Create practical AI business systems and portfolio-ready implementations for consulting or freelancing',
            'Earn a verified Winning Blueprints certificate with hands-on AI business execution experience',
        ],
        'includes': [
            '8 weeks of on-demand video content', 'Completion certificate',
            'Hands-on business AI projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': [
            'AI Business Foundations', 'AI Productivity Systems', 'Sales & Marketing with AI',
            'Customer Support Automation', 'Operations Automation', 'AI Business Growth Systems',
            'Implementation & Consulting', 'Capstone & Execution',
        ],
        'ideal_paths': [
            'AI Business Consultant', 'Business Automation Specialist', 'AI Operations Associate',
            'Process Automation Executive', 'AI Implementation Consultant',
        ],
        'overview': [
            'Learn practical AI implementation for real business growth — designed for entrepreneurs, business owners, managers, and beginners entering AI implementation.',
            'Focus on execution, automation, and measurable business outcomes across productivity, sales, marketing, support, and operations.',
            'Real business applications: lead generation automation, sales follow-up workflows, customer support automation, reporting automation, and growth system design.',
            'Hands-on projects include AI productivity setup, marketing automation campaign, support workflow design, and business operations automation.',
            'Final capstone: build a complete AI transformation system for a business with portfolio documentation and implementation presentation.',
        ],
        'curriculum': [
            _mod('AI Business Foundations', [
                'Introduction to AI for business owners', 'Understanding AI opportunities in SMEs',
                'Business process mapping fundamentals', 'AI tools ecosystem overview',
                'Identifying automation opportunities', 'Assignment: business workflow audit',
                'AI implementation mindset',
            ], True),
            _mod('AI Productivity Systems', [
                'AI productivity tools setup', 'Prompt engineering for business tasks',
                'Email drafting with AI', 'Proposal and quotation generation',
                'Document summarization workflows', 'AI meeting productivity tools',
                'Assignment: executive productivity system',
            ], True),
            _mod('Sales & Marketing with AI', [
                'AI lead generation workflows', 'Digital marketing automation basics',
                'AI content creation for business', 'Sales messaging automation',
                'Customer acquisition systems', 'Social media automation workflows',
                'Assignment: AI marketing campaign',
            ]),
            _mod('Customer Support Automation', [
                'AI chatbot fundamentals', 'Customer response automation', 'FAQ automation systems',
                'Support workflow design', 'CRM workflow basics', 'Customer communication automation',
                'Assignment: support automation blueprint',
            ]),
            _mod('Operations Automation', [
                'Invoice automation workflows', 'Reporting automation systems', 'Task management automation',
                'Internal communication automation', 'Data entry reduction workflows',
                'Business process optimization', 'Assignment: operations automation project',
            ]),
            _mod('AI Business Growth Systems', [
                'Growth strategy with AI', 'AI-powered decision support', 'Competitor research automation',
                'Business intelligence basics', 'Customer retention workflows',
                'Revenue growth automation concepts', 'Assignment: growth system design',
            ]),
            _mod('Implementation & Consulting', [
                'AI implementation project planning', 'Client discovery process',
                'Business automation consulting basics', 'Pricing AI implementation services',
                'Proposal structuring', 'Delivery workflow design',
                'Assignment: mock AI consulting engagement',
            ]),
            _mod('Capstone & Execution', [
                'Final business AI system planning', 'Capstone implementation', 'Portfolio documentation',
                'Business transformation roadmap', 'Implementation presentation',
                'Freelance and consulting launch strategy', 'Final business AI showcase',
            ]),
        ],
        'career': {'min': '₹3L', 'max': '₹12L', 'label': 'Entry to senior roles'},
        'reviews': [
            {'quote': 'I implemented AI workflows for quotations, customer responses, and internal reporting. The time savings alone made this course highly valuable for my business.', 'name': 'Vikas Shah', 'role': 'Manufacturing Business Owner', 'city': 'Ahmedabad'},
            {'quote': 'The course made AI practical instead of overwhelming. I now use automation workflows daily and positioned myself for better operational roles.', 'name': 'Neha Bansal', 'role': 'Business Operations Executive', 'city': 'Delhi'},
            {'quote': 'The consulting and implementation modules helped me package AI services for SMEs. I gained real confidence in delivering automation solutions.', 'name': 'Rohan Kulkarni', 'role': 'Automation Consultant', 'city': 'Pune'},
        ],
        'highlight_quote': 'I implemented AI workflows for quotations, customer responses, and internal reporting.',
        'highlight_author': 'Vikas Shah, Manufacturing Business Owner',
        'starts_with': 'AI Business Foundations',
    },
    {
        'slug': 'digital-marketing-with-ai',
        'title': 'AI-Powered Digital Marketing Mastery',
        'goal': (
            'Master AI-powered digital marketing, SEO, ads, and automation with hands-on campaigns — '
            'built for beginners seeking jobs, freelancing, or business growth.'
        ),
        'level': 'Intermediate',
        'duration': '12 weeks',
        'format': 'Self-paced',
        'modules_count': 12,
        'topics_count': 84,
        'price': '₹16,999',
        'salary_range': '₹3–12 LPA',
        'featured': True,
        'enrolled': 83,
        'rating': 5.0,
        'reviews_count': 3,
        'image': img('photo-1460925895917-afdab827c52f', 800, 500),
        'gains': [
            'Build real digital marketing campaigns using AI tools across SEO, content, and paid ads',
            'Create portfolio-ready marketing projects for freelancing, jobs, or business growth',
            'Earn a verified Winning Blueprints certificate with practical implementation experience',
        ],
        'includes': [
            '12 weeks of on-demand video content', 'Completion certificate',
            'Hands-on campaign projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': [
            'Digital Marketing Foundations', 'AI Tools for Marketers', 'SEO with AI',
            'Content Marketing Systems', 'Social Media Marketing', 'Paid Ads Mastery',
            'Performance Marketing', 'Email & Automation Marketing', 'Analytics & Reporting',
            'Freelancing & Client Delivery', 'Advanced AI Marketing Workflows', 'Capstone & Career Launch',
        ],
        'ideal_paths': [
            'Digital Marketing Executive', 'SEO Executive', 'Performance Marketing Associate',
            'Social Media Manager', 'AI Marketing Specialist', 'Content Marketing Executive',
        ],
        'overview': [
            'Learn practical digital marketing with AI using a beginner-friendly, implementation-first approach for students, freelancers, business owners, and aspiring marketers in India.',
            'Build SEO optimization, paid advertising, AI content workflows, social media growth, email automation, and marketing analytics skills.',
            'Real-world projects: SEO website optimization, social media growth campaign, paid ads blueprint, automated email funnel, and AI content production workflow.',
            'Prepare for entry-level digital marketing roles, build an interview-ready portfolio, and learn freelance client acquisition and delivery.',
            'Final capstone: build a complete AI-powered digital marketing campaign with audience targeting, content, ads, automation, and reporting.',
        ],
        'curriculum': [
            _mod('Digital Marketing Foundations', [
                'Introduction to digital marketing', 'Marketing channels overview', 'Customer journey fundamentals',
                'Digital marketing terminology', 'AI in modern marketing overview',
                'Assignment: market analysis basics', 'Marketing campaign planning',
            ], True),
            _mod('AI Tools for Marketers', [
                'Introduction to AI marketing tools', 'Prompt engineering for marketers',
                'AI content generation workflows', 'AI research automation', 'Marketing productivity tools',
                'AI image and design tools', 'Assignment: AI marketing toolkit setup',
            ], True),
            _mod('SEO with AI', [
                'SEO fundamentals', 'Keyword research with AI', 'On-page SEO optimization',
                'Technical SEO basics', 'AI content optimization', 'SEO audit workflows',
                'Assignment: optimize a website page',
            ]),
            _mod('Content Marketing Systems', [
                'Content strategy fundamentals', 'Blog content planning', 'AI copywriting workflows',
                'Content calendars', 'Email content creation', 'Content repurposing systems',
                'Assignment: content campaign creation',
            ]),
            _mod('Social Media Marketing', [
                'Social platform strategy', 'Audience building methods', 'AI social content creation',
                'Reel and short video strategy', 'Engagement growth tactics',
                'Posting workflow automation', 'Assignment: social campaign launch',
            ]),
            _mod('Paid Ads Mastery', [
                'Meta Ads fundamentals', 'Google Ads basics', 'Campaign objective selection',
                'Audience targeting strategy', 'Ad copy with AI', 'Budget optimization basics',
                'Assignment: ad campaign blueprint',
            ]),
            _mod('Performance Marketing', [
                'Conversion funnel design', 'Landing page optimization', 'Retargeting concepts',
                'Campaign KPI tracking', 'Conversion rate basics', 'Performance optimization workflows',
                'Assignment: conversion audit',
            ]),
            _mod('Email & Automation Marketing', [
                'Email marketing fundamentals', 'Lead nurturing workflows', 'Marketing automation basics',
                'AI email writing', 'Segmentation concepts', 'Drip campaign setup',
                'Assignment: automated email funnel',
            ]),
            _mod('Analytics & Reporting', [
                'Marketing analytics basics', 'Google Analytics concepts', 'Campaign reporting',
                'Traffic analysis', 'AI reporting automation', 'Dashboard interpretation',
                'Assignment: reporting dashboard',
            ]),
            _mod('Freelancing & Client Delivery', [
                'Digital marketing freelancing basics', 'Client acquisition methods', 'Proposal creation',
                'Service pricing strategy', 'Campaign reporting for clients',
                'Client communication workflows', 'Assignment: mock client project',
            ]),
            _mod('Advanced AI Marketing Workflows', [
                'AI campaign automation', 'Lead generation systems', 'Multi-channel campaign orchestration',
                'Marketing workflow optimization', 'Scaling campaign operations',
                'Advanced AI productivity systems', 'Assignment: AI automation campaign',
            ]),
            _mod('Capstone & Career Launch', [
                'Final campaign project planning', 'Portfolio creation', 'Interview preparation',
                'Resume building for marketing jobs', 'Freelancing launch roadmap',
                'Campaign presentation', 'Career action plan',
            ]),
        ],
        'career': {'min': '₹3L', 'max': '₹12L', 'label': 'Entry to senior roles'},
        'reviews': [
            {'quote': 'The AI SEO and content modules helped me confidently handle real client projects. I landed my first marketing role within weeks of completing the course.', 'name': 'Rohit Agarwal', 'role': 'SEO Executive', 'city': 'Jaipur'},
            {'quote': 'The paid ads and automation workflows were practical and easy to implement. I started offering social media and ad management services to local businesses.', 'name': 'Sneha Kulkarni', 'role': 'Freelance Digital Marketer', 'city': 'Pune'},
            {'quote': 'This course gave me hands-on campaign experience instead of just theory. The capstone project became a strong portfolio piece for interviews.', 'name': 'Arjun Nair', 'role': 'Growth Marketing Associate', 'city': 'Bengaluru'},
        ],
        'highlight_quote': 'The AI SEO and content modules helped me confidently handle real client projects.',
        'highlight_author': 'Rohit Agarwal, SEO Executive',
        'starts_with': 'Digital Marketing Foundations',
    },
    {
        'slug': 'prompt-engineering-mastery-pem',
        'title': 'Prompt Engineering Mastery (PEM)',
        'goal': 'Learn how to communicate with AI like a professional.',
        'level': 'Beginner',
        'duration': '4 weeks',
        'format': 'Self-paced',
        'modules_count': 4,
        'topics_count': 28,
        'price': '₹2,999',
        'salary_range': None,
        'featured': False,
        'enrolled': 47,
        'rating': 5.0,
        'reviews_count': 0,
        'image': img('photo-1677442136019-21780ecad995', 800, 500),
        'gains': [
            'Job-ready skills with structured, self-paced lessons',
            'Earn a verified Winning Blueprints certificate recognized by employers',
            'Design high-performing prompts that generate accurate, structured, and monetizable outputs',
        ],
        'includes': [
            '4 weeks of on-demand content', 'Completion certificate',
            'Hands-on assignments & projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': ['AI Basics', 'Core Prompting', 'Advanced Techniques', 'Business Use Cases'],
        'ideal_paths': ['Prompt Specialist', 'AI Content Consultant', 'Freelance Prompt Designer'],
        'overview': [
            'Learn how to communicate with AI like a professional. Design high-performing prompts that generate accurate, structured, and monetizable outputs.',
            'Duration: 4 weeks at 60 min/day. Covers LLM fundamentals, role prompting, instruction design, chain of thought, few-shot prompting, and business use cases.',
            'Project: create 50+ reusable prompts and build a sellable prompt pack.',
            'Outcome: become a Prompt Specialist and sell prompts or freelance services.',
        ],
        'curriculum': [
            _mod('AI Basics', [
                'LLM fundamentals', 'Tokens, temperature, context',
            ], True),
            _mod('Core Prompting', [
                'Role prompting', 'Instruction design', 'Output formatting',
            ], True),
            _mod('Advanced Techniques', [
                'Chain of Thought', 'Few-shot prompting', 'Prompt chaining',
            ]),
            _mod('Business Use Cases', [
                'Content generation', 'Sales copy', 'Automation prompts',
            ]),
        ],
        'career': None,
        'reviews': [],
        'highlight_quote': 'Learn how to design high-performing prompts that generate accurate, structured outputs.',
        'highlight_author': 'Winning Blueprints Academy',
        'starts_with': 'AI Basics',
    },
    {
        'slug': 'ai-automation-builder-aab',
        'title': 'AI Automation Builder (AAB)',
        'goal': 'Build systems that replace manual work with AI workflows. Learn automation using no-code + Python.',
        'level': 'Intermediate',
        'duration': '4 weeks',
        'format': 'Self-paced',
        'modules_count': 4,
        'topics_count': 24,
        'price': '₹3,999',
        'salary_range': None,
        'featured': False,
        'enrolled': 47,
        'rating': 5.0,
        'reviews_count': 0,
        'image': img('photo-1518186285589-2f7649de56e0', 800, 500),
        'gains': [
            'Job-ready skills with structured, self-paced lessons',
            'Earn a verified Winning Blueprints certificate recognized by employers',
            'Build automation services and save 100+ hours/month with workflow systems',
        ],
        'includes': [
            '4 weeks of on-demand content', 'Completion certificate',
            'Hands-on assignments & projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': ['Automation Basics', 'Tools', 'Data Automation', 'Communication Automation'],
        'ideal_paths': ['Automation Builder', 'Workflow Specialist', 'No-Code Developer'],
        'overview': [
            'Build systems that replace manual work with AI workflows using no-code tools and Python fundamentals.',
            'Covers Zapier/Make, APIs, webhooks, scraping basics, lead generation bots, email automation, and WhatsApp workflows.',
            'Projects: lead generation bot and auto email sender.',
            'Outcome: build automation services and save 100+ hours/month.',
        ],
        'curriculum': [
            _mod('Automation Basics', ['What is automation', 'Workflow thinking'], True),
            _mod('Tools', ['Zapier / Make', 'APIs', 'Webhooks']),
            _mod('Data Automation', ['Scraping basics', 'Lead generation bots']),
            _mod('Communication Automation', ['Email automation', 'WhatsApp workflows']),
        ],
        'career': None,
        'reviews': [],
        'highlight_quote': 'Build systems that replace manual work with AI workflows.',
        'highlight_author': 'Winning Blueprints Academy',
        'starts_with': 'Automation Basics',
    },
    {
        'slug': 'ai-tools-for-freelancers',
        'title': 'AI Tools for Freelancers',
        'goal': 'Use AI to deliver faster and win high-value clients.',
        'level': 'All levels',
        'duration': '4 weeks',
        'format': 'Self-paced',
        'modules_count': 4,
        'topics_count': 20,
        'price': '₹3,999',
        'salary_range': None,
        'featured': False,
        'enrolled': 47,
        'rating': 5.0,
        'reviews_count': 0,
        'image': img('photo-1522071820081-009f0129c71c', 800, 500),
        'gains': [
            'Job-ready skills with structured, self-paced lessons',
            'Earn a verified Winning Blueprints certificate recognized by employers',
            'Deliver faster with AI and package services for high-value clients',
        ],
        'includes': [
            '4 weeks of on-demand content', 'Completion certificate',
            'Hands-on assignments & projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': ['AI Productivity', 'Client Delivery', 'Service Packaging', 'Freelance Growth'],
        'ideal_paths': ['Freelance Consultant', 'AI Service Provider', 'Digital Freelancer'],
        'overview': [
            'Prompt design, content workflows, automation, and service packaging for freelancers who want to win higher-value clients.',
            'Learn to use AI tools to deliver projects faster, improve proposals, and scale your freelance business.',
        ],
        'curriculum': [
            _mod('AI Productivity for Freelancers', [
                'AI toolkit setup', 'Prompt design for client work', 'Faster content delivery',
            ], True),
            _mod('Client Delivery Workflows', [
                'Project scoping with AI', 'Revision workflows', 'Quality control systems',
            ]),
            _mod('Service Packaging', [
                'Pricing AI-enabled services', 'Proposal templates', 'Portfolio positioning',
            ]),
            _mod('Freelance Growth', [
                'Client acquisition', 'Upselling automation services', 'Scaling with AI',
            ]),
        ],
        'career': None,
        'reviews': [],
        'highlight_quote': 'Use AI to deliver faster and win high-value clients.',
        'highlight_author': 'Winning Blueprints Academy',
        'starts_with': 'AI Productivity for Freelancers',
    },
    {
        'slug': 'e-commerce-growth-manager-pro',
        'title': 'E-Commerce Growth Manager Pro',
        'goal': 'Master e-commerce growth, client communication, and revenue-focused sales systems.',
        'level': 'Intermediate',
        'duration': '4 weeks',
        'format': 'Self-paced',
        'modules_count': 4,
        'topics_count': 20,
        'price': '₹9,999',
        'salary_range': None,
        'featured': False,
        'enrolled': 47,
        'rating': 5.0,
        'reviews_count': 0,
        'image': img('photo-1556742049-0cfed4f6a45d', 800, 500),
        'gains': [
            'Job-ready skills with structured, self-paced lessons',
            'Earn a verified Winning Blueprints certificate recognized by employers',
            'Close more clients with confident communication and conversion systems',
        ],
        'includes': [
            '4 weeks of on-demand content', 'Completion certificate',
            'Hands-on assignments & projects', 'Live mentor Q&A support',
            'Mobile & desktop access', 'Lifetime access',
        ],
        'learn_modules': ['E-Commerce Foundations', 'Growth Strategy', 'Sales Communication', 'Revenue Systems'],
        'ideal_paths': ['E-Commerce Manager', 'Growth Consultant', 'Sales Executive', 'D2C Operator'],
        'overview': [
            'Discovery calls, objection handling, and conversion scripts for e-commerce revenue growth.',
            'Learn practical systems for scaling online stores, managing client relationships, and driving measurable sales outcomes.',
        ],
        'curriculum': [
            _mod('E-Commerce Foundations', [
                'D2C business models', 'Store optimization basics', 'Customer journey mapping',
            ], True),
            _mod('Growth Strategy', [
                'Acquisition channels', 'Retention systems', 'Campaign planning',
            ]),
            _mod('Sales Communication', [
                'Discovery calls', 'Objection handling', 'Conversion scripts',
            ]),
            _mod('Revenue Systems', [
                'Reporting dashboards', 'Client delivery workflows', 'Scaling operations',
            ]),
        ],
        'career': None,
        'reviews': [],
        'highlight_quote': 'Close more clients with confident communication and conversion systems.',
        'highlight_author': 'Winning Blueprints Academy',
        'starts_with': 'E-Commerce Foundations',
    },
]


def get_course(slug):
    return next((c for c in COURSES if c['slug'] == slug), None)


def get_featured_courses():
    return [c for c in COURSES if c.get('featured')]
