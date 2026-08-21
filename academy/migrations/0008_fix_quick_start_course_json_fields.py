from django.db import migrations


def _mod(title, topics, free_preview=False):
    return {'title': title, 'topics': topics, 'free_preview': free_preview}


FIXED_FIELDS = {
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
    'reviews': [],
}


def fix_course(apps, schema_editor):
    """The quick-start-digital-marketing course got manually recreated through
    the ops 'Add a course' UI before the seed migration (0007) could run, with
    Python-list-literal text pasted into the one-item-per-line JSON fields —
    e.g. 'gains' ended up as a 1-item list containing the str() of the whole
    list instead of 3 separate strings. get_or_create in 0007 then found this
    row already existed and left it alone. Force-fix it here unconditionally."""
    CourseListing = apps.get_model('academy', 'CourseListing')
    CourseListing.objects.filter(slug='quick-start-digital-marketing').update(**FIXED_FIELDS)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0007_seed_quick_start_course'),
    ]

    operations = [
        migrations.RunPython(fix_course, noop),
    ]
