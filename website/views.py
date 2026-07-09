from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .data import (
    ACADEMY_PROCESS,
    CASE_STUDIES,
    CLIENT_LOGOS,
    CONTACT_INFO,
    INDUSTRIES,
    MODEL_STEPS,
    PRICING_FAQS,
    PRICING_TIERS,
    RECENT_PROJECTS,
    SERVICE_PROCESS,
    SERVICES,
    STATS,
    TEAM_ROLES,
    TESTIMONIALS,
    WHY_CHOOSE_US,
)
from .forms import LeadForm
from .services import create_lead


def _page(request, template, title, description='', **extra):
    return render(request, template, {
        'page_title': title,
        'meta_description': description,
        **extra,
    })


def home(request):
    return _page(
        request,
        'pages/home.jinja',
        'Home',
        'Grow your business with AI, digital marketing, and web technology. Trusted growth partner for modern businesses.',
        form=LeadForm(),
        services=SERVICES,
        why_choose_us=WHY_CHOOSE_US,
        recent_projects=RECENT_PROJECTS,
        team_roles=TEAM_ROLES,
        model_steps=MODEL_STEPS,
        stats=STATS,
        client_logos=CLIENT_LOGOS,
        testimonials=TESTIMONIALS,
        service_process=SERVICE_PROCESS,
        pricing_tiers=PRICING_TIERS,
        pricing_faqs=PRICING_FAQS[:4],
        industries=INDUSTRIES[:6],
        featured_case_study=CASE_STUDIES[0],
    )


def services(request):
    return _page(
        request,
        'pages/services.jinja',
        'Services',
        'SEO, Google Ads, Meta Ads, web development, automation, CRM, branding, and content marketing.',
        form=LeadForm(),
        services=SERVICES,
        why_choose_us=WHY_CHOOSE_US,
        service_process=SERVICE_PROCESS,
        stats=STATS,
        client_logos=CLIENT_LOGOS,
        recent_projects=RECENT_PROJECTS[:3],
    )


def service_detail(request, slug):
    service = next((s for s in SERVICES if s['slug'] == slug), None)
    if not service:
        from django.http import Http404
        raise Http404('Service not found')
    return _page(
        request,
        'pages/service_detail.jinja',
        service['title'],
        service['short'],
        form=LeadForm(initial={'service_interest': service['title']}),
        service=service,
        all_services=SERVICES,
    )


def our_work(request):
    return _page(
        request,
        'pages/our_work.jinja',
        'Our Work',
        'Recent client projects across websites, SEO, lead generation, AI, and automation.',
        projects=RECENT_PROJECTS,
        case_studies=CASE_STUDIES,
        services=SERVICES,
    )


def case_studies(request):
    return _page(
        request,
        'pages/case_studies.jinja',
        'Case Studies',
        'Real results from real clients. See how we drive growth across industries.',
        case_studies=CASE_STUDIES,
    )


def case_study_detail(request, slug):
    study = next((c for c in CASE_STUDIES if c['slug'] == slug), None)
    if not study:
        from django.http import Http404
        raise Http404('Case study not found')
    related = [c for c in CASE_STUDIES if c['slug'] != slug][:2]
    return _page(
        request,
        'pages/case_study_detail.jinja',
        study['title'],
        study['summary'],
        study=study,
        related=related,
    )


def industries(request):
    return _page(
        request,
        'pages/industries.jinja',
        'Industries',
        'Digital growth solutions tailored for SaaS, e-commerce, healthcare, real estate, and more.',
        industries=INDUSTRIES,
    )


def pricing(request):
    return _page(
        request,
        'pages/pricing.jinja',
        'Pricing',
        'Transparent pricing packages for digital marketing and growth services.',
        pricing_tiers=PRICING_TIERS,
        pricing_faqs=PRICING_FAQS,
    )


def about(request):
    return _page(
        request,
        'pages/about.jinja',
        'About',
        'Winning Blueprints is a professional digital growth company helping businesses scale with AI and marketing.',
        why_choose_us=WHY_CHOOSE_US,
        stats=STATS,
        team_roles=TEAM_ROLES,
        model_steps=MODEL_STEPS,
    )


def careers(request):
    return _page(
        request,
        'pages/careers.jinja',
        'Careers',
        'Join our internship program. Learn while working on real client projects with senior experts.',
        academy_process=ACADEMY_PROCESS,
        stats=STATS,
        team_roles=TEAM_ROLES,
    )


def contact(request):
    form = LeadForm()
    return _page(
        request,
        'pages/contact.jinja',
        'Contact',
        'Book a free strategy call or send us a message. We respond within 24 hours.',
        form=form,
        contact_info=CONTACT_INFO,
    )


@require_http_methods(['GET', 'POST'])
def lead_submit(request):
    form = LeadForm(request.POST or None)
    source = request.POST.get('source_page', request.GET.get('source_page', ''))

    if request.method == 'POST' and form.is_valid():
        create_lead(form, source_page=source)
        return render(request, 'partials/_lead_success.jinja', {
            'message': 'Thank you! We will contact you within 24 hours.',
        })

    return render(request, 'partials/_lead_form.jinja', {
        'form': form,
        'source_page': source,
        'show_errors': request.method == 'POST',
    })
