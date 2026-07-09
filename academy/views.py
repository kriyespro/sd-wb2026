from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from website.data import ACADEMY_PROCESS

from .courses_data import COURSES, get_course
from .forms import AdmissionApplicationForm
from .services import create_admission_application


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
