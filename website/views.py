from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from academy.models import CourseListing

from . import content
from .data import LP_AI_DM_COMPARISON
from .forms import JobApplicationForm, JobPostSubmissionForm, LeadForm
from .models import JobOpening
from .services import create_job_application, create_lead, get_existing_job_application


def _open_roles():
    return JobOpening.objects.filter(is_active=True, status=JobOpening.STATUS_APPROVED)


def _role_titles():
    return list(_open_roles().values_list('title', flat=True))


def _role_title_from_slug(slug):
    role = _open_roles().filter(slug=slug).first()
    return role.title if role else ''


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
        services=content.services(),
        why_choose_us=content.why_choose_us(),
        recent_projects=content.recent_projects(),
        team=content.team_preview(),
        team_roles=content.team_roles(),
        model_steps=content.model_steps(),
        stats=content.stats(),
        audience_tags=content.audience_tags(),
        testimonials=content.testimonials(),
        service_process=content.f2c_pipeline(),
        f2c_pipeline=content.f2c_pipeline(),
        flagship_offers=content.flagship_offers(),
        pricing_tiers=content.pricing_tiers(),
        pricing_faqs=content.faqs('pricing')[:4],
        general_faqs=content.faqs('general'),
        industries=content.industries()[:6],
        hero_points=content.hero_points(),
        featured_case_study=content.case_studies().first(),
    )


def services(request):
    return _page(
        request,
        'pages/services.jinja',
        'Services',
        'eCommerce setup, Meta & Google ads, WhatsApp automation, backoffice SOPs — built for textile manufacturers going D2C.',
        form=LeadForm(),
        services=content.services(),
        why_choose_us=content.why_choose_us(),
        service_process=content.f2c_pipeline(),
        flagship_offers=content.flagship_offers(),
        stats=content.stats(),
        audience_tags=content.audience_tags(),
        recent_projects=content.recent_projects()[:3],
    )


def service_detail(request, slug):
    service = content.service_by_slug(slug)
    if not service:
        raise Http404('Service not found')
    return _page(
        request,
        'pages/service_detail.jinja',
        service.title,
        service.short,
        form=LeadForm(initial={'service_interest': service.title}),
        service=service,
        all_services=content.services(),
    )


def our_work(request):
    return _page(
        request,
        'pages/our_work.jinja',
        'Our Work',
        'Factory-to-customer projects: stores, Meta ads, Google Shopping, and backoffice systems for manufacturers.',
        projects=content.recent_projects(),
        case_studies=content.case_studies(),
        services=content.services(),
    )


def case_studies(request):
    return _page(
        request,
        'pages/case_studies.jinja',
        'Case Studies',
        'Real manufacturers. Real prepaid orders. See how factories go direct-to-customer with Winning Blueprints.',
        case_studies=content.case_studies(),
    )


def case_study_detail(request, slug):
    study = content.case_study_by_slug(slug)
    if not study:
        raise Http404('Case study not found')
    related = content.case_studies().exclude(slug=slug)[:2]
    return _page(
        request,
        'pages/case_study_detail.jinja',
        study.title,
        study.summary,
        study=study,
        related=related,
    )


def industries(request):
    return _page(
        request,
        'pages/industries.jinja',
        'Industries',
        'D2C growth systems for textile manufacturers, garment factories, saree brands, and emerging fashion labels.',
        industries=content.industries(),
    )


def pricing(request):
    return _page(
        request,
        'pages/pricing.jinja',
        'Pricing',
        'Flexible D2C plans from ₹15K/month — store, ads, and backoffice tailored to your factory.',
        pricing_tiers=content.pricing_tiers(),
        pricing_faqs=content.faqs('pricing'),
        general_faqs=content.faqs('general'),
    )


def about(request):
    return _page(
        request,
        'pages/about.jinja',
        'About',
        'Winning Blueprints helps textile manufacturers sell direct to customers — powered by a delivery team and internal academy.',
        why_choose_us=content.why_choose_us(),
        stats=content.stats(),
        team=content.team_preview(),
        team_roles=content.team_roles(),
        model_steps=content.model_steps(),
        f2c_pipeline=content.f2c_pipeline(),
    )


def team(request):
    return _page(
        request,
        'pages/team.jinja',
        'Our Team',
        'Meet the Winning Blueprints team — 100+ specialists helping manufacturers sell direct.',
        founders=content.founders(),
        core_team=content.core_team(),
        departments=content.team_departments(),
        stats=content.stats(),
    )


def startup(request):
    return _page(
        request,
        'pages/startup.jinja',
        'Startup Plan',
        'Full Startup Plan: build the product, create & train the team, plan marketing & ops, then launch — idea to income.',
        form=LeadForm(initial={'service_interest': 'Full Startup Plan'}),
        phases=content.startup_phases(),
        promises=content.startup_promises(),
        startup_for=content.startup_for(),
        startup_faqs=content.faqs('startup'),
        stats=content.stats(),
    )


def careers(request):
    role_slug = request.GET.get('role', '')
    role_title = _role_title_from_slug(role_slug)
    initial = {'role': role_title} if role_title else {}
    if role_title and 'Intern' in role_title:
        initial['application_type'] = 'internship'
    form = JobApplicationForm(initial=initial, role_choices=_role_titles())
    return _page(
        request,
        'pages/careers.jinja',
        'Careers',
        'Open roles at Winning Blueprints — full-time and internship. Apply directly for jobs on real D2C and startup work.',
        form=form,
        open_roles=_open_roles(),
        careers_perks=content.careers_perks(),
        academy_process=content.academy_process(),
        stats=content.stats(),
        team_roles=content.team_roles(),
    )


def join(request):
    return _page(
        request,
        'pages/join.jinja',
        'Join',
        'Create your Winning Blueprints account — business client, student, DGC partner, or apply to the team.',
    )


@require_http_methods(['GET', 'POST'])
def post_job(request):
    submitted = False
    form = JobPostSubmissionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        submitted = True
        form = JobPostSubmissionForm()
    return _page(
        request,
        'pages/post_job.jinja',
        'Post a Job',
        'Advertise your open role to the Winning Blueprints talent network — reviewed by our team before it goes live.',
        form=form,
        submitted=submitted,
        show_errors=request.method == 'POST' and not submitted,
    )


@require_http_methods(['GET', 'POST'])
def job_apply_submit(request):
    form = JobApplicationForm(request.POST or None, role_choices=_role_titles())
    if request.method == 'POST' and form.is_valid():
        existing = get_existing_job_application(
            form.cleaned_data.get('email'), form.cleaned_data.get('phone'),
        )
        if existing:
            return render(request, 'partials/_job_apply_duplicate.jinja', {'application': existing})
        create_job_application(form)
        return render(request, 'partials/_job_apply_success.jinja')

    # Non-HTMX full-page POST fallback
    if request.method == 'POST' and not request.headers.get('HX-Request'):
        return _page(
            request,
            'pages/careers.jinja',
            'Careers',
            'Open roles at Winning Blueprints — full-time and internship.',
            form=form,
            open_roles=_open_roles(),
            careers_perks=content.careers_perks(),
            academy_process=content.academy_process(),
            stats=content.stats(),
            team_roles=content.team_roles(),
            show_errors=True,
        )

    return render(request, 'partials/_job_apply_form.jinja', {
        'form': form,
        'show_errors': request.method == 'POST',
        'open_roles': _open_roles(),
    })


def contact(request):
    form = LeadForm()
    return _page(
        request,
        'pages/contact.jinja',
        'Contact',
        'Book a free strategy call or send us a message. We respond within 24 hours.',
        form=form,
        contact_info=content.contact_info(),
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


LP_AI_DM_SLUG = 'quick-start-digital-marketing'
LP_AI_DM_SOURCE = 'meta_ads_ai_digital_marketing'


def lp_ai_digital_marketing(request):
    """Standalone, distraction-free landing page for Meta Ads traffic.
    Backed by the existing 'Winning Blueprints Digital Launchpad' course
    listing — price stays the single source of truth, editable in
    /ops/courses/, instead of forking a duplicate catalog row."""
    course = CourseListing.objects.filter(slug=LP_AI_DM_SLUG, is_active=True).first()
    if not course:
        raise Http404('Course not found')
    mentor = content.mentor_for_role('Marketing Expert')
    return render(request, 'pages/lp/ai_digital_marketing.jinja', {
        'page_title': 'Winning Blueprints Digital Launchpad — 4 Weeks, ₹999',
        'meta_description': (
            'Vibe Coding + Meta Ads + Google Ads + Client Handling in 4 weeks for ₹999. '
            '12 live online classes, practical assignments, beginner-friendly.'
        ),
        'course': course,
        'faqs': content.faqs('lp_ai_dm'),
        'comparison': LP_AI_DM_COMPARISON,
        'mentor': mentor,
        'contact_info': content.contact_info(),
        'meta_pixel_id': settings.META_PIXEL_ID,
        'lead_source': LP_AI_DM_SOURCE,
        'form': LeadForm(),
    })


@require_http_methods(['GET', 'POST'])
def lp_ai_digital_marketing_lead(request):
    form = LeadForm(request.POST or None)
    dom_id = request.POST.get('dom_id') or 'lp-lead-form-container'
    if request.method == 'POST' and form.is_valid():
        create_lead(form, source_page=LP_AI_DM_SOURCE)
        return render(request, 'partials/_lp_lead_success.jinja', {'dom_id': dom_id})

    return render(request, 'partials/_lp_lead_form.jinja', {
        'form': form,
        'lead_source': LP_AI_DM_SOURCE,
        'dom_id': dom_id,
        'show_errors': request.method == 'POST',
    })
