from datetime import date, timedelta

from django.contrib.auth import get_user_model

from .models import (
    AdmissionApplication,
    Assignment,
    Attendance,
    Certificate,
    Course,
    Enrollment,
    MentorAllocation,
    PlacementApplication,
    PortfolioItem,
    StudentProject,
    StudentTask,
    Submission,
)

User = get_user_model()

STUDENT_NAV = [
    {'title': 'Courses', 'icon': '📚', 'url_name': 'academy_dashboard:courses'},
    {'title': 'Assignments', 'icon': '✏️', 'url_name': 'academy_dashboard:assignments'},
    {'title': 'Tasks', 'icon': '✅', 'url_name': 'academy_dashboard:tasks'},
    {'title': 'Projects', 'icon': '🚀', 'url_name': 'academy_dashboard:projects'},
    {'title': 'Mentor', 'icon': '👨‍🏫', 'url_name': 'academy_dashboard:mentor'},
    {'title': 'Attendance', 'icon': '📋', 'url_name': 'academy_dashboard:attendance'},
    {'title': 'Portfolio', 'icon': '💼', 'url_name': 'academy_dashboard:portfolio'},
    {'title': 'Certificates', 'icon': '🏆', 'url_name': 'academy_dashboard:certificates'},
    {'title': 'Interview Prep', 'icon': '🎤', 'url_name': 'academy_dashboard:interview_prep'},
    {'title': 'Placement', 'icon': '🎯', 'url_name': 'academy_dashboard:placement'},
]


def get_student_stats(user):
    enrollments = Enrollment.objects.filter(user=user)
    course_ids = enrollments.values_list('course_id', flat=True)
    pending_assignments = Assignment.objects.filter(course_id__in=course_ids).exclude(
        submissions__user=user,
    ).count()
    return {
        'courses_count': enrollments.count(),
        'pending_assignments': pending_assignments,
        'open_tasks': StudentTask.objects.filter(user=user).exclude(status=StudentTask.STATUS_DONE).count(),
        'active_projects': StudentProject.objects.filter(
            user=user, status=StudentProject.STATUS_ACTIVE,
        ).count(),
        'portfolio_count': PortfolioItem.objects.filter(user=user).count(),
        'certificates_count': Certificate.objects.filter(user=user).count(),
    }


def get_enrolled_courses(user):
    return Course.objects.filter(
        enrollments__user=user, enrollments__status=Enrollment.STATUS_ACTIVE,
    ).distinct()


def get_student_assignments(user):
    course_ids = Enrollment.objects.filter(user=user).values_list('course_id', flat=True)
    return Assignment.objects.filter(course_id__in=course_ids).select_related('course')


def submit_assignment(user, assignment, content):
    submission, _ = Submission.objects.update_or_create(
        user=user, assignment=assignment,
        defaults={'content': content, 'status': Submission.STATUS_SUBMITTED},
    )
    return submission


def add_portfolio_item(user, form):
    item = form.save(commit=False)
    item.user = user
    item.save()
    return item


def create_admission_application(form):
    return form.save()


def get_mentor_for_student(user):
    try:
        return user.mentor_allocation.mentor
    except MentorAllocation.DoesNotExist:
        return None
