from django.db import migrations


def _mod(title, topics, free_preview=False):
    return {'title': title, 'topics': topics, 'free_preview': free_preview}


COURSE = {
    'slug': 'quick-start-digital-marketing',
    'title': 'Quick Start Digital Marketing',
    'goal': (
        'Get a practical, AI-powered introduction to digital marketing in just 4 weeks — '
        'learn the core channels, run your first campaign, and build one real project for '
        'your portfolio.'
    ),
    'level': 'Beginner',
    'duration': '4 weeks',
    'format': 'Self-paced',
    'modules_count': 4,
    'topics_count': 16,
    'price': '₹999',
    'salary_range': '₹2–5 LPA',
    'featured': False,
    'enrolled': 0,
    'rating': 0,
    'reviews_count': 0,
    'image': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=800&h=500&q=70',
    'gains': [
        'Understand the core digital marketing channels and where AI actually saves you time',
        'Write, publish, and optimize your first AI-assisted content and SEO piece',
        'Launch and read the results of your first small paid ad campaign',
    ],
    'includes': [
        '4 weeks of on-demand video lessons',
        'Completion certificate',
        '1 guided hands-on project',
        'Community support',
        'Mobile & desktop access',
        'Lifetime access to course updates',
    ],
    'learn_modules': [
        'Digital Marketing Foundations', 'AI-Powered Content & SEO Basics',
        'Running Your First Paid Ad', 'Portfolio Project & Next Steps',
    ],
    'ideal_paths': [
        'Digital Marketing Trainee', 'Freelance Starter', 'Marketing Intern', 'Social Media Assistant',
    ],
    'overview': [
        'Most digital marketing courses either drown you in theory or take six months to get '
        'to the part where you actually run a campaign. This one skips straight to doing.',
        'Over 4 weeks, you cover the core channels — SEO, content, and paid ads — using the same '
        'AI tools working marketers use daily to move faster: drafting copy, researching '
        'keywords, and reading campaign data.',
        'You finish with one real project in your portfolio and a working knowledge of the full '
        'digital marketing stack, so you can decide whether to specialize, freelance, or go '
        'deeper with a full program.',
    ],
    'curriculum': [
        _mod('Digital Marketing Foundations', [
            'What digital marketing means today', 'Core channels: SEO, social, paid, email',
            'How AI fits into every channel', 'Setting a starter marketing goal',
        ], True),
        _mod('AI-Powered Content & SEO Basics', [
            'Using AI tools to draft content and headlines', 'On-page SEO basics for beginners',
            'Keyword research with AI prompts', 'Publishing your first optimized post',
        ]),
        _mod('Running Your First Paid Ad', [
            'Meta Ads Manager walkthrough', 'Setting a small test budget',
            'Writing ad copy with AI assistance', 'Reading basic ad metrics',
        ]),
        _mod('Portfolio Project & Next Steps', [
            'Build one real campaign case study', 'Package your portfolio for freelancing/jobs',
            'Where to go next: specialize or scale', 'Q&A and wrap-up',
        ]),
    ],
    'career_label': 'Foundational entry roles', 'career_min': '₹2L', 'career_max': '₹5L',
    'reviews': [],
    'highlight_quote': (
        'I built this as the fastest way to go from zero to your first real campaign — '
        'no fluff, just the AI workflows I use daily.'
    ),
    'highlight_author': 'ShreeVastav Mayank, Marketing Expert & Mentor',
    'starts_with': 'Digital Marketing Foundations',
    'is_active': True,
    'sort_order': 9,
}


def seed_course(apps, schema_editor):
    CourseListing = apps.get_model('academy', 'CourseListing')
    CourseListing.objects.get_or_create(slug=COURSE['slug'], defaults=COURSE)


def unseed_course(apps, schema_editor):
    CourseListing = apps.get_model('academy', 'CourseListing')
    CourseListing.objects.filter(slug=COURSE['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0006_seed_course_listings'),
    ]

    operations = [
        migrations.RunPython(seed_course, unseed_course),
    ]
