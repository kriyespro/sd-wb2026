from projects.models import Deliverable, Meeting, Project, Report

from .models import ClientAccount, SupportMessage, SupportTicket

CLIENT_NAV = [
    {'title': 'Projects', 'icon': '📁', 'url_name': 'clients:projects'},
    {'title': 'Reports', 'icon': '📊', 'url_name': 'clients:reports'},
    {'title': 'Files', 'icon': '📎', 'url_name': 'clients:files'},
    {'title': 'Meetings', 'icon': '📅', 'url_name': 'clients:meetings'},
    {'title': 'Invoices', 'icon': '🧾', 'url_name': 'clients:invoices'},
    {'title': 'Support', 'icon': '💬', 'url_name': 'clients:support'},
    {'title': 'Analytics', 'icon': '📈', 'url_name': 'clients:analytics'},
    {'title': 'Goals', 'icon': '🎯', 'url_name': 'clients:goals'},
    {'title': 'ROI', 'icon': '💰', 'url_name': 'clients:roi'},
]


def get_client_account(user):
    return getattr(user, 'client_account', None)


def get_client_projects(account):
    if not account:
        return Project.objects.none()
    return account.projects.all()


def get_approved_deliverables(account):
    """Only mentor/QA-approved deliverables are ever exposed to clients."""
    if not account:
        return Deliverable.objects.none()
    return Deliverable.objects.filter(
        project__client_account=account,
        approval_status=Deliverable.APPROVAL_APPROVED,
    ).select_related('project')


def get_client_reports(account):
    if not account:
        return Report.objects.none()
    return Report.objects.filter(project__client_account=account).select_related('project')


def get_client_meetings(account):
    if not account:
        return Meeting.objects.none()
    return account.meetings.all()


def get_client_stats(account):
    if not account:
        return {
            'active_projects': 0,
            'approved_files': 0,
            'upcoming_meetings': 0,
            'open_tickets': 0,
        }
    return {
        'active_projects': account.projects.filter(status=Project.STATUS_ACTIVE).count(),
        'approved_files': get_approved_deliverables(account).count(),
        'upcoming_meetings': account.meetings.filter(status=Meeting.STATUS_SCHEDULED).count(),
        'open_tickets': account.tickets.exclude(status=SupportTicket.STATUS_RESOLVED).count(),
    }


def create_ticket(account, subject, body, sender):
    ticket = SupportTicket.objects.create(client_account=account, subject=subject)
    SupportMessage.objects.create(ticket=ticket, sender=sender, body=body)
    return ticket


def add_ticket_reply(ticket, body, sender):
    return SupportMessage.objects.create(ticket=ticket, sender=sender, body=body)
