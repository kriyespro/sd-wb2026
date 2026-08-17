from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from . import fourd_services
from .models import (
    ActivityLog,
    AdmissionApplication,
    Assignment,
    Attendance,
    Certificate,
    Course,
    DailyFourD,
    Enrollment,
    MentorAllocation,
    PlacementApplication,
    PortfolioItem,
    StudentLead,
    StudentProject,
    StudentTask,
    Submission,
    TeachingSession,
)

User = get_user_model()

STUDENT_NAV = [
    {'title': 'Daily 4D', 'icon': '🎯', 'url_name': 'academy_dashboard:fourd', 'new': True},
    {'title': 'My Progress', 'icon': '📈', 'url_name': 'academy_dashboard:progress', 'new': True},
    {'title': 'Courses', 'icon': '📚', 'url_name': 'academy_dashboard:courses'},
    {'title': 'Assignments', 'icon': '✏️', 'url_name': 'academy_dashboard:assignments'},
    {'title': 'Teaching', 'icon': '🗣️', 'url_name': 'academy_dashboard:teaching', 'new': True},
    {'title': 'Field CRM', 'icon': '📞', 'url_name': 'academy_dashboard:field_leads', 'new': True},
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


def mark_task_done(task):
    task.status = StudentTask.STATUS_DONE
    task.completed_at = timezone.now()
    task.save(update_fields=['status', 'completed_at'])
    return task


def create_teaching_session(user, cleaned_data):
    return TeachingSession.objects.create(user=user, **cleaned_data)


def evaluate_teaching_session(session, evaluator, score, feedback):
    session.status = TeachingSession.STATUS_EVALUATED
    session.evaluated_by = evaluator
    session.score = score
    session.feedback = feedback
    session.evaluated_at = timezone.now()
    session.save(update_fields=['status', 'evaluated_by', 'score', 'feedback', 'evaluated_at'])
    return session


def create_student_lead(user, cleaned_data):
    return StudentLead.objects.create(user=user, **cleaned_data)


def update_student_lead_status(lead, status):
    lead.status = status
    lead.save(update_fields=['status', 'updated_at'])
    return lead


def save_daily_notes(user, log_date, notes):
    log, _ = DailyFourD.objects.update_or_create(
        user=user, date=log_date, defaults={'notes': notes},
    )
    return log


def log_activity(user, cleaned_data):
    return ActivityLog.objects.create(user=user, **cleaned_data)


def get_student_attention_items(user):
    """Priority alerts for the student dashboard header."""
    items = []

    stats = get_student_stats(user)
    if stats['pending_assignments']:
        n = stats['pending_assignments']
        items.append({
            'label': f"{n} assignment{'s' if n != 1 else ''} due",
            'href_name': 'academy_dashboard:assignments',
            'tone': 'amber',
        })

    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    if not any(fourd_services.pillar_status(user, today).values()):
        streak_active = any(fourd_services.pillar_status(user, yesterday).values())
        items.append({
            'label': "4D streak at risk — log today" if streak_active else "Log today's 4D",
            'href_name': 'academy_dashboard:fourd',
            'tone': 'orange',
        })

    new_feedback = TeachingSession.objects.filter(
        user=user, status=TeachingSession.STATUS_EVALUATED,
        evaluated_at__gte=timezone.now() - timedelta(days=3),
    ).count()
    if new_feedback:
        items.append({
            'label': f"{new_feedback} new teaching review{'s' if new_feedback != 1 else ''}",
            'href_name': 'academy_dashboard:teaching',
            'tone': 'emerald',
        })

    open_leads = StudentLead.objects.filter(user=user, status=StudentLead.STATUS_NEW).count()
    if open_leads:
        items.append({
            'label': f"{open_leads} lead{'s' if open_leads != 1 else ''} need follow-up",
            'href_name': 'academy_dashboard:field_leads',
            'tone': 'teal',
        })

    return items
