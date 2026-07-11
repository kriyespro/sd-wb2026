from django.utils import timezone

from academy.models import AdmissionApplication, MentorAllocation
from projects.models import Deliverable, Project
from website.models import JobApplication, Lead

from .models import ProjectAssignment, Team, TeamMember

OPS_NAV = [
    {'title': 'Quality Check', 'icon': '✔️', 'url_name': 'operations:quality_check'},
    {'title': 'Projects', 'icon': '📁', 'url_name': 'operations:projects'},
    {'title': 'Talent Pipeline', 'icon': '🔄', 'url_name': 'operations:pipeline'},
    {'title': 'Project Allocation', 'icon': '🔗', 'url_name': 'operations:allocation'},
    {'title': 'Mentor Allocation', 'icon': '🎓', 'url_name': 'operations:mentors'},
    {'title': 'Team', 'icon': '👥', 'url_name': 'operations:team'},
    {'title': 'Performance', 'icon': '📊', 'url_name': 'operations:performance'},
    {'title': 'Leads', 'icon': '📞', 'url_name': 'operations:leads'},
    {'title': 'Invoices', 'icon': '🧾', 'url_name': 'operations:invoices'},
]

# Superuser-only nav items (appended in OpsBaseMixin)
OPS_NAV_SUPERUSER = [
    {'title': 'Job Applications', 'icon': '💼', 'url_name': 'operations:job_applications'},
]


def get_pending_deliverables():
    return Deliverable.objects.filter(
        approval_status=Deliverable.APPROVAL_PENDING,
    ).select_related('project', 'project__client_account')


def approve_deliverable(deliverable, approver):
    deliverable.approval_status = Deliverable.APPROVAL_APPROVED
    deliverable.approved_by = approver
    deliverable.save(update_fields=['approval_status', 'approved_by'])
    return deliverable


def reject_deliverable(deliverable, approver):
    deliverable.approval_status = Deliverable.APPROVAL_REJECTED
    deliverable.approved_by = approver
    deliverable.save(update_fields=['approval_status', 'approved_by'])
    return deliverable


def get_ops_stats():
    return {
        'pending_deliverables': get_pending_deliverables().count(),
        'active_projects': Project.objects.filter(status=Project.STATUS_ACTIVE).count(),
        'new_applications': AdmissionApplication.objects.filter(
            status=AdmissionApplication.STATUS_NEW,
        ).count(),
        'new_leads': Lead.objects.filter(status=Lead.STATUS_NEW).count(),
        'new_job_applications': JobApplication.objects.filter(
            status=JobApplication.STATUS_NEW,
        ).count(),
        'total_job_applications': JobApplication.objects.count(),
    }


def get_recent_leads(limit=10):
    return Lead.objects.select_related(
        'assigned_to', 'converted_client',
    ).order_by('-created_at')[:limit]


def get_lead_pipeline_counts():
    return {
        status: Lead.objects.filter(status=status).count()
        for status, _ in Lead.STATUS_CHOICES
    }


def get_recent_applications(limit=5):
    return AdmissionApplication.objects.filter(
        status=AdmissionApplication.STATUS_NEW,
    ).order_by('-created_at')[:limit]


def get_recent_job_applications(limit=8):
    return JobApplication.objects.order_by('-created_at')[:limit]


def get_attention_items(stats, include_jobs=False):
    """Priority alerts for the mission control header."""
    items = []
    if stats['new_leads']:
        items.append({
            'label': f"{stats['new_leads']} new lead{'s' if stats['new_leads'] != 1 else ''}",
            'href_name': 'operations:leads',
            'tone': 'emerald',
        })
    if stats['pending_deliverables']:
        items.append({
            'label': f"{stats['pending_deliverables']} pending QA",
            'href_name': 'operations:quality_check',
            'tone': 'orange',
        })
    if stats['new_applications']:
        items.append({
            'label': f"{stats['new_applications']} academy app{'s' if stats['new_applications'] != 1 else ''}",
            'href_name': 'operations:pipeline',
            'tone': 'brand',
        })
    if include_jobs and stats['new_job_applications']:
        items.append({
            'label': f"{stats['new_job_applications']} job application{'s' if stats['new_job_applications'] != 1 else ''}",
            'href_name': 'operations:job_applications',
            'tone': 'violet',
        })
    return items


def get_mission_control_context(include_jobs=False):
    stats = get_ops_stats()
    ctx = {
        'stats': stats,
        'recent_leads': get_recent_leads(10),
        'pending_deliverables': get_pending_deliverables()[:5],
        'lead_pipeline': get_lead_pipeline_counts(),
        'recent_applications': get_recent_applications(5),
        'attention_items': get_attention_items(stats, include_jobs=include_jobs),
        'updated_at': timezone.localtime(),
        'include_jobs': include_jobs,
    }
    if include_jobs:
        ctx['recent_job_applications'] = get_recent_job_applications(8)
        ctx['job_application_new'] = stats['new_job_applications']
        ctx['job_application_count'] = stats['total_job_applications']
    return ctx


def validate_project_staffing(project):
    """Enforce: every project needs 1 PM (owner) and 1 senior specialist (tech lead)."""
    roles = set(project.assignments.values_list('role', flat=True))
    issues = []
    if ProjectAssignment.ROLE_PM not in roles:
        issues.append('Missing Project Manager (owner)')
    if ProjectAssignment.ROLE_SENIOR not in roles:
        issues.append('Missing Senior Specialist (tech lead)')
    return issues


def get_teams():
    return Team.objects.prefetch_related('members__user')
