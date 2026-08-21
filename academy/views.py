import razorpay
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from website.data import ACADEMY_PROCESS, STATS, TEAM_CORE

from .forms import AdmissionApplicationForm
from .models import AdmissionApplication
from .services import (
    create_admission_application,
    create_course_payment_order,
    get_active_courses,
    get_course_listing,
    get_featured_courses,
    verify_course_payment,
)


def home(request):
    return courses(request)


def courses(request):
    return render(request, 'pages/academy/courses.jinja', {
        'page_title': 'Courses',
        'meta_description': (
            'Explore practical, outcome-focused programs — clear pricing, duration, '
            'and career paths on every course page.'
        ),
        'courses': get_active_courses(),
        'featured_courses': get_featured_courses(),
    })


def course_detail(request, slug):
    course = get_course_listing(slug)
    if not course:
        raise Http404('Course not found')
    other_courses = get_active_courses().exclude(slug=slug)[:3]
    mentor = next((m for m in TEAM_CORE if m['role'] == 'Marketing Expert'), None)
    return render(request, 'pages/academy/course_detail.jinja', {
        'page_title': course.title,
        'meta_description': course.goal[:160],
        'course': course,
        'other_courses': other_courses,
        'mentor': mentor,
        'academy_stats': STATS,
    })


def checkout(request, slug):
    course = get_course_listing(slug)
    if not course:
        raise Http404('Course not found')

    prefill_name, prefill_email, prefill_phone = '', '', ''
    if request.user.is_authenticated:
        prefill_name = request.user.get_full_name() or request.user.username
        prefill_email = request.user.email
        prefill_phone = getattr(getattr(request.user, 'profile', None), 'phone', '')

    return render(request, 'pages/academy/checkout.jinja', {
        'page_title': f"Checkout — {course.title}",
        'meta_description': f"Complete your purchase of {course.title}.",
        'course': course,
        'prefill_name': prefill_name,
        'prefill_email': prefill_email,
        'prefill_phone': prefill_phone,
    })


def apply(request):
    form = AdmissionApplicationForm()
    return render(request, 'pages/academy/apply.jinja', {
        'page_title': 'Apply',
        'meta_description': 'Apply to Winning Blueprints Academy.',
        'form': form,
        'academy_process': ACADEMY_PROCESS,
        'courses': get_active_courses(),
    })


@require_http_methods(['GET', 'POST'])
def apply_submit(request):
    form = AdmissionApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        create_admission_application(form)
        return render(request, 'partials/_admission_success.jinja')

    return render(request, 'partials/_admission_form.jinja', {
        'form': form,
        'show_errors': request.method == 'POST',
    })


@require_POST
def enroll_pay(request, slug):
    course = get_course_listing(slug)
    if not course:
        raise Http404('Course not found')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()

    try:
        application, order = create_course_payment_order(course, name=name, email=email, phone=phone)
    except razorpay.errors.BadRequestError:
        return render(request, 'partials/dashboard/_checkout_launch.jinja', {
            'error': 'Could not start payment. Please try again.',
        })

    return render(request, 'partials/dashboard/_checkout_launch.jinja', {
        'dom_id': f'admission-{application.pk}',
        'description': course.title,
        'order_id': order['id'],
        'amount_paise': order['amount'],
        'key_id': settings.RAZORPAY_KEY_ID,
        'verify_url': reverse('academy:enroll_verify', kwargs={'slug': slug, 'pk': application.pk}),
        'prefill_name': name,
        'prefill_email': email,
    })


@require_POST
def enroll_verify(request, slug, pk):
    application = get_object_or_404(AdmissionApplication, pk=pk)
    try:
        verify_course_payment(
            application,
            request.POST.get('razorpay_order_id', ''),
            request.POST.get('razorpay_payment_id', ''),
            request.POST.get('razorpay_signature', ''),
        )
        return render(request, 'pages/academy/enroll_result.jinja', {
            'page_title': 'Enrollment confirmed', 'success': True, 'application': application,
        })
    except (ValueError, razorpay.errors.SignatureVerificationError):
        return render(request, 'pages/academy/enroll_result.jinja', {
            'page_title': 'Payment verification failed', 'success': False,
        })
