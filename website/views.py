from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .data import (
    ACADEMY_PROCESS,
    AUDIENCE_TAGS,
    CASE_STUDIES,
    CONTACT_INFO,
    F2C_PIPELINE,
    FLAGSHIP_OFFERS,
    GENERAL_FAQS,
    HERO_POINTS,
    INDUSTRIES,
    MODEL_STEPS,
    PRICING_FAQS,
    PRICING_TIERS,
    RECENT_PROJECTS,
    SERVICE_PROCESS,
    SERVICES,
    STATS,
    TEAM,
    TEAM_CORE,
    TEAM_DEPARTMENTS,
    TEAM_FOUNDERS,
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
        'We help textile manufacturers sell sarees, t-shirts, jeans, and kurtis directly to customers — online, prepaid, with 2x–4x higher margins.',
        form=LeadForm(),
        services=SERVICES,
        why_choose_us=WHY_CHOOSE_US,
        recent_projects=RECENT_PROJECTS,
        team=TEAM,
        team_roles=TEAM_ROLES,
        model_steps=MODEL_STEPS,
        stats=STATS,
        audience_tags=AUDIENCE_TAGS,
        testimonials=TESTIMONIALS,
        service_process=SERVICE_PROCESS,
        f2c_pipeline=F2C_PIPELINE,
        flagship_offers=FLAGSHIP_OFFERS,
        pricing_tiers=PRICING_TIERS,
        pricing_faqs=PRICING_FAQS[:4],
        general_faqs=GENERAL_FAQS,
        industries=INDUSTRIES[:6],
        hero_points=HERO_POINTS,
        featured_case_study=CASE_STUDIES[0],
    )


def services(request):
    return _page(
        request,
        'pages/services.jinja',
        'Services',
        'eCommerce setup, Meta & Google ads, WhatsApp automation, backoffice SOPs — built for textile manufacturers going D2C.',
        form=LeadForm(),
        services=SERVICES,
        why_choose_us=WHY_CHOOSE_US,
        service_process=SERVICE_PROCESS,
        flagship_offers=FLAGSHIP_OFFERS,
        stats=STATS,
        audience_tags=AUDIENCE_TAGS,
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
        'Factory-to-customer projects: stores, Meta ads, Google Shopping, and backoffice systems for manufacturers.',
        projects=RECENT_PROJECTS,
        case_studies=CASE_STUDIES,
        services=SERVICES,
    )


def case_studies(request):
    return _page(
        request,
        'pages/case_studies.jinja',
        'Case Studies',
        'Real manufacturers. Real prepaid orders. See how factories go direct-to-customer with Winning Blueprints.',
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
        'D2C growth systems for textile manufacturers, garment factories, saree brands, and emerging fashion labels.',
        industries=INDUSTRIES,
    )


def pricing(request):
    return _page(
        request,
        'pages/pricing.jinja',
        'Pricing',
        'Flexible D2C plans from ₹15K/month — store, ads, and backoffice tailored to your factory.',
        pricing_tiers=PRICING_TIERS,
        pricing_faqs=PRICING_FAQS,
        general_faqs=GENERAL_FAQS,
    )


def about(request):
    return _page(
        request,
        'pages/about.jinja',
        'About',
        'Winning Blueprints helps textile manufacturers sell direct to customers — powered by a delivery team and internal academy.',
        why_choose_us=WHY_CHOOSE_US,
        stats=STATS,
        team=TEAM,
        team_roles=TEAM_ROLES,
        model_steps=MODEL_STEPS,
        f2c_pipeline=F2C_PIPELINE,
    )


def team(request):
    return _page(
        request,
        'pages/team.jinja',
        'Our Team',
        'Meet the Winning Blueprints team — 100+ specialists helping manufacturers sell direct.',
        founders=TEAM_FOUNDERS,
        core_team=TEAM_CORE,
        departments=TEAM_DEPARTMENTS,
        stats=STATS,
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
