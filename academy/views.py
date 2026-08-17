import razorpay
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from website.data import ACADEMY_PROCESS

from .courses_data import COURSES, get_course
from .forms import AdmissionApplicationForm
from .models import AdmissionApplication
from .services import create_admission_application, create_course_payment_order, verify_course_payment


def home(request):
    return courses(request)


def courses(request):
    return render(request, 'pages/academy/courses.jinja', {
        'page_title': 'Courses',
        'meta_description': (
            'Explore practical, outcome-focused programs — clear pricing, duration, '
            'and career paths on every course page.'
        ),
        'courses': COURSES,
        'featured_courses': [c for c in COURSES if c.get('featured')],
    })


def course_detail(request, slug):
    course = get_course(slug)
    if not course:
        raise Http404('Course not found')
    other_courses = [c for c in COURSES if c['slug'] != slug][:3]
    return render(request, 'pages/academy/course_detail.jinja', {
        'page_title': course['title'],
        'meta_description': course['goal'][:160],
        'course': course,
        'other_courses': other_courses,
    })


def apply(request):
    form = AdmissionApplicationForm()
    return render(request, 'pages/academy/apply.jinja', {
        'page_title': 'Apply',
        'meta_description': 'Apply to Winning Blueprints Academy.',
        'form': form,
        'academy_process': ACADEMY_PROCESS,
        'courses': COURSES,
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
    course = get_course(slug)
    if not course:
        raise Http404('Course not found')

    try:
        application, order = create_course_payment_order(course)
    except razorpay.errors.BadRequestError:
        return render(request, 'partials/dashboard/_checkout_launch.jinja', {
            'error': 'Could not start payment. Please try again.',
        })

    return render(request, 'partials/dashboard/_checkout_launch.jinja', {
        'dom_id': f'admission-{application.pk}',
        'description': course['title'],
        'order_id': order['id'],
        'amount_paise': order['amount'],
        'key_id': settings.RAZORPAY_KEY_ID,
        'verify_url': reverse('academy:enroll_verify', kwargs={'slug': slug, 'pk': application.pk}),
        'prefill_name': '',
        'prefill_email': '',
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
