"""Query helpers backing the public pages — replaces the hardcoded
constants that used to live in website/data.py (see website/migrations/
0010_cms_models.py + 0011_seed_cms_content.py). Most content models use
the exact same field names the templates already expect, so those are
returned as querysets/instances directly; the few sections whose original
dict keys don't match a model field name (FAQ q/a, team roles/departments'
`count`) are mapped into plain dicts here so no template needs to change."""

from django.core.cache import cache

from .models import (
    CaseStudy,
    FAQ,
    PricingTier,
    ProjectBlock,
    Service,
    SiteSettings,
    StartupPhase,
    StatBlock,
    TeamMember,
    Testimonial,
    TitleDescBlock,
)


def _blocks(section):
    return TitleDescBlock.objects.filter(section=section, is_active=True).order_by('order', 'id')


def why_choose_us():
    return _blocks(TitleDescBlock.SECTION_WHY_CHOOSE_US)


def startup_promises():
    return _blocks(TitleDescBlock.SECTION_STARTUP_PROMISES)


def startup_for():
    return _blocks(TitleDescBlock.SECTION_STARTUP_FOR)


def f2c_pipeline():
    return _blocks(TitleDescBlock.SECTION_F2C_PIPELINE)


def model_steps():
    return _blocks(TitleDescBlock.SECTION_MODEL_STEPS)


def industries():
    return _blocks(TitleDescBlock.SECTION_INDUSTRIES)


def careers_perks():
    return _blocks(TitleDescBlock.SECTION_CAREERS_PERKS)


def team_departments():
    return [
        {'icon': b.icon, 'title': b.title, 'count': b.badge, 'desc': b.desc}
        for b in _blocks(TitleDescBlock.SECTION_TEAM_DEPARTMENTS)
    ]


def team_roles():
    return [
        {'role': b.title, 'count': b.badge, 'image': b.image}
        for b in _blocks(TitleDescBlock.SECTION_TEAM_ROLES)
    ]


def academy_process():
    return [b.title for b in _blocks(TitleDescBlock.SECTION_ACADEMY_PROCESS)]


def audience_tags():
    return [b.title for b in _blocks(TitleDescBlock.SECTION_AUDIENCE_TAGS)]


def hero_points():
    return [b.title for b in _blocks(TitleDescBlock.SECTION_HERO_POINTS)]


def stats():
    return StatBlock.objects.filter(is_active=True).order_by('order', 'id')


def recent_projects():
    return ProjectBlock.objects.filter(is_active=True).order_by('order', 'id')


def testimonials():
    return Testimonial.objects.filter(is_active=True).order_by('order', 'id')


def faqs(group):
    return [{'q': f.question, 'a': f.answer} for f in FAQ.objects.filter(group=group, is_active=True).order_by('order', 'id')]


def founders():
    return TeamMember.objects.filter(is_founder=True, is_active=True).order_by('order', 'id')


def core_team():
    return TeamMember.objects.filter(is_founder=False, is_active=True).order_by('order', 'id')


def team_preview():
    """Home / about preview — founders + first two core (was
    TEAM = TEAM_FOUNDERS + TEAM_CORE[:2])."""
    return list(founders()) + list(core_team()[:2])


def mentor_for_role(role):
    return TeamMember.objects.filter(role=role, is_active=True).first()


def services():
    return Service.objects.filter(is_active=True).order_by('order', 'id')


def service_by_slug(slug):
    return Service.objects.filter(slug=slug, is_active=True).first()


def flagship_offers():
    return [
        {'title': s.title, 'icon': s.icon, 'short': s.short, 'features': s.flagship_features, 'slug': s.slug, 'popular': s.popular}
        for s in Service.objects.filter(is_active=True, is_flagship=True).order_by('order', 'id')
    ]


def case_studies():
    return CaseStudy.objects.filter(is_active=True).order_by('order', 'id')


def case_study_by_slug(slug):
    return CaseStudy.objects.filter(slug=slug, is_active=True).first()


def pricing_tiers():
    return PricingTier.objects.filter(is_active=True).order_by('order', 'id')


def startup_phases():
    return StartupPhase.objects.filter(is_active=True).order_by('order', 'id')


def site_settings():
    """5-minute cache — contact/hero images change rarely; avoids a query
    on every public page load. Bust manually by clearing the cache key if
    an edit needs to show up immediately (acceptable staleness otherwise)."""
    settings_obj = cache.get('cms:site_settings')
    if settings_obj is None:
        settings_obj = SiteSettings.load()
        cache.set('cms:site_settings', settings_obj, 300)
    return settings_obj


def site_images():
    s = site_settings()
    return {'hero': s.hero_image, 'contact_bg': s.contact_bg_image, 'about_team': s.about_team_image}


def contact_info():
    s = site_settings()
    return {'email': s.contact_email, 'phone': s.contact_phone, 'address': s.contact_address, 'hours': s.contact_hours}
