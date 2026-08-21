from django.db import migrations


def _mod(title, topics, free_preview=False):
    return {'title': title, 'topics': topics, 'free_preview': free_preview}


REBRAND = {
    'title': 'Winning Blueprints Digital Launchpad',
    'goal': (
        'A practical 4-week live bootcamp covering AI-assisted coding, Meta Ads, Google Ads, and '
        'client handling — 12 live online sessions to help you build, advertise, communicate, and '
        'execute like a digital professional.'
    ),
    'level': 'Beginner',
    'duration': '4 weeks',
    'format': 'Live online',
    'modules_count': 4,
    'topics_count': 54,
    'salary_range': '',
    'gains': [
        'Build a basic AI-assisted website or landing page from scratch',
        'Plan, launch, and manage a real Meta Ads lead-generation campaign',
        'Run a complete Google Search Ads campaign from keyword to landing page',
        'Confidently approach, communicate with, and handle real client work',
    ],
    'includes': [
        '4 weeks of live online training — 12 live classes',
        'Vibe Coding, Meta Ads, Google Ads & Client Handling modules',
        'Practical assignments & real-world scenarios',
        'Live Q&A support',
        'Completion certificate',
        'Beginner-friendly guidance throughout',
    ],
    'learn_modules': [
        'Vibe Coding (AI-Assisted Development)', 'Meta Ads', 'Google Ads', 'Client Handling',
    ],
    'ideal_paths': [
        'Freelancer', 'Digital Marketing Trainee', 'Agency Assistant', 'Small Business / Solo Founder',
    ],
    'overview': [
        "Knowing only one skill isn't enough anymore. This bootcamp teaches four skills that "
        'connect — build a landing page with AI, run Meta and Google ad campaigns to generate '
        'leads, then talk to and handle a real client — across 12 live online sessions over 4 weeks.',
        "You won't just watch videos. Each week follows the same loop: learn, practice, build, "
        'apply — one skill per week, with practical tasks throughout instead of passive lectures.',
        "By the end you'll have worked on an AI-assisted website, a Meta Ads campaign structure, a "
        'Google Ads campaign structure, and a real client proposal — not just theory.',
        'This is training, not a guarantee. Results depend on your own practice, execution, and '
        'follow-through after the bootcamp ends.',
    ],
    'curriculum': [
        _mod('Vibe Coding (AI-Assisted Development)', [
            'AI-assisted coding', 'Prompting AI for development', 'Website structure & UI',
            'Landing page creation', 'Frontend basics', 'Working with AI coding tools',
            'Debugging with AI', 'Improving existing websites', 'Deploying a basic project',
            'Turning an idea into a working MVP',
        ], True),
        _mod('Meta Ads', [
            'Meta Business Manager', 'Ad account setup', 'Campaign structure', 'Campaign objectives',
            'Audience research', 'Targeting', 'Creative strategy', 'Ad copy',
            'Lead generation campaigns', 'WhatsApp lead campaigns', 'Budget planning',
            'Campaign launch', 'Basic optimization', 'Reading campaign data', 'Understanding CPL',
            'Common lead ad mistakes',
        ]),
        _mod('Google Ads', [
            'Google Ads fundamentals', 'Search campaign structure', 'Keyword research',
            'Search intent', 'Match types', 'Negative keywords', 'Ad copy', 'Landing pages',
            'Conversion tracking concepts', 'Campaign setup', 'Budget planning', 'Bid strategy',
            'Search term analysis', 'Basic optimization', 'Measuring campaign performance',
        ]),
        _mod('Client Handling', [
            'How to find potential clients', 'How to approach a business', 'How to introduce yourself',
            'Understanding client requirements', 'What questions to ask before starting',
            'How to explain your services', 'How to discuss pricing', 'How to create a proposal',
            'How to communicate professionally', 'How to handle client objections',
            'How to report campaign performance', 'How to handle difficult situations',
            'How to retain clients',
        ]),
    ],
    'career_label': '', 'career_min': '', 'career_max': '',
    'reviews': [],
    'highlight_quote': (
        "This isn't a course you watch — it's four skills you practice until they connect: "
        'build, advertise, communicate, execute.'
    ),
    'highlight_author': 'Winning Blueprints Academy',
    'starts_with': 'Introduction to AI-Powered Development',
}


def rebrand_course(apps, schema_editor):
    """Rename/rewrite the quick-start-digital-marketing course into the new
    4-skill 'Digital Launchpad' bootcamp positioning (Vibe Coding + Meta Ads +
    Google Ads + Client Handling), keeping the same slug/URL/checkout so
    nothing already linking to it breaks."""
    CourseListing = apps.get_model('academy', 'CourseListing')
    CourseListing.objects.filter(slug='quick-start-digital-marketing').update(**REBRAND)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_fix_quick_start_course_json_fields'),
    ]

    operations = [
        migrations.RunPython(rebrand_course, noop),
    ]
