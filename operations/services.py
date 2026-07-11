from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from academy.models import AdmissionApplication
from billing.models import Invoice
from projects.models import Deliverable, Project
from website.models import JobApplication, Lead

from .models import ProjectAssignment, Team

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
    {'title': 'DGC Applications', 'icon': '🤝', 'url_name': 'operations:dgc_applications'},
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


def _local_day_start():
    now = timezone.localtime()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def get_ops_stats():
    day_start = _local_day_start()
    week_start = day_start - timedelta(days=7)
    month_start = day_start.replace(day=1)
    open_lead_statuses = [
        Lead.STATUS_NEW,
        Lead.STATUS_CONTACTED,
        Lead.STATUS_QUALIFIED,
        Lead.STATUS_PROPOSAL,
    ]

    job_counts = {
        row['status']: row['c']
        for row in JobApplication.objects.values('status').annotate(c=Count('id'))
    }

    return {
        'pending_deliverables': get_pending_deliverables().count(),
        'active_projects': Project.objects.filter(status=Project.STATUS_ACTIVE).count(),
        'planning_projects': Project.objects.filter(status=Project.STATUS_PLANNING).count(),
        'new_applications': AdmissionApplication.objects.filter(
            status=AdmissionApplication.STATUS_NEW,
        ).count(),
        'new_leads': Lead.objects.filter(status=Lead.STATUS_NEW).count(),
        'leads_today': Lead.objects.filter(created_at__gte=day_start).count(),
        'leads_week': Lead.objects.filter(created_at__gte=week_start).count(),
        'unassigned_leads': Lead.objects.filter(
            assigned_to__isnull=True,
            status__in=open_lead_statuses,
        ).count(),
        'hot_leads': Lead.objects.filter(
            status__in=[Lead.STATUS_QUALIFIED, Lead.STATUS_PROPOSAL],
        ).count(),
        'won_month': Lead.objects.filter(
            status=Lead.STATUS_WON,
            updated_at__gte=month_start,
        ).count(),
        'open_pipeline': Lead.objects.filter(status__in=open_lead_statuses).count(),
        'overdue_invoices': Invoice.objects.filter(status=Invoice.STATUS_OVERDUE).count(),
        'sent_invoices': Invoice.objects.filter(status=Invoice.STATUS_SENT).count(),
        'new_job_applications': job_counts.get(JobApplication.STATUS_NEW, 0),
        'job_review': job_counts.get(JobApplication.STATUS_REVIEW, 0),
        'job_interview': job_counts.get(JobApplication.STATUS_INTERVIEW, 0),
        'total_job_applications': sum(job_counts.values()),
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
    if stats['unassigned_leads']:
        items.append({
            'label': f"{stats['unassigned_leads']} unassigned",
            'href_name': 'operations:leads',
            'tone': 'amber',
        })
    if stats['pending_deliverables']:
        items.append({
            'label': f"{stats['pending_deliverables']} pending QA",
            'href_name': 'operations:quality_check',
            'tone': 'orange',
        })
    if stats['overdue_invoices']:
        items.append({
            'label': f"{stats['overdue_invoices']} overdue invoice{'s' if stats['overdue_invoices'] != 1 else ''}",
            'href_name': 'operations:invoices',
            'tone': 'rose',
        })
    if stats['new_applications']:
        items.append({
            'label': f"{stats['new_applications']} academy app{'s' if stats['new_applications'] != 1 else ''}",
            'href_name': 'operations:pipeline',
            'tone': 'brand',
        })
    if include_jobs and stats['new_job_applications']:
        items.append({
            'label': f"{stats['new_job_applications']} job app{'s' if stats['new_job_applications'] != 1 else ''}",
            'href_name': 'operations:job_applications',
            'tone': 'violet',
        })
    return items


def get_mission_control_context(include_jobs=False):
    stats = get_ops_stats()
    pipeline = get_lead_pipeline_counts()
    pipeline_total = sum(pipeline.values()) or 1
    ctx = {
        'stats': stats,
        'recent_leads': get_recent_leads(8),
        'pending_deliverables': get_pending_deliverables()[:6],
        'lead_pipeline': pipeline,
        'pipeline_total': pipeline_total,
        'recent_applications': get_recent_applications(5),
        'attention_items': get_attention_items(stats, include_jobs=include_jobs),
        'updated_at': timezone.localtime(),
        'include_jobs': include_jobs,
    }
    if include_jobs:
        ctx['recent_job_applications'] = get_recent_job_applications(6)
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
