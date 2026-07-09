from academy.models import AdmissionApplication, MentorAllocation
from projects.models import Deliverable, Project
from website.models import Lead

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
    }


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
