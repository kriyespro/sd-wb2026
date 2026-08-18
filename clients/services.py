from datetime import timedelta

from django.utils import timezone

from billing.models import Invoice
from projects.models import Deliverable, Meeting, Milestone, Project, Report

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
    {'title': 'Post a Job', 'icon': '📢', 'url_name': 'clients:post_job'},
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


def get_client_attention_items(account):
    """Priority alerts for the client dashboard header."""
    items = []
    if not account:
        return items

    overdue_invoices = Invoice.objects.filter(
        client_account=account, status=Invoice.STATUS_OVERDUE,
    ).count()
    if overdue_invoices:
        items.append({
            'label': f"{overdue_invoices} overdue invoice{'s' if overdue_invoices != 1 else ''}",
            'href_name': 'clients:invoices',
            'tone': 'rose',
        })

    today = timezone.localdate()
    overdue_milestones = Milestone.objects.filter(
        project__client_account=account, due_date__lt=today,
    ).exclude(status=Milestone.STATUS_DONE).count()
    if overdue_milestones:
        items.append({
            'label': f"{overdue_milestones} milestone{'s' if overdue_milestones != 1 else ''} overdue",
            'href_name': 'clients:projects',
            'tone': 'orange',
        })

    week_end = today + timedelta(days=7)
    upcoming_meetings = account.meetings.filter(
        status=Meeting.STATUS_SCHEDULED,
        scheduled_at__date__gte=today, scheduled_at__date__lte=week_end,
    ).count()
    if upcoming_meetings:
        items.append({
            'label': f"{upcoming_meetings} meeting{'s' if upcoming_meetings != 1 else ''} this week",
            'href_name': 'clients:meetings',
            'tone': 'brand',
        })

    # A ticket needs the client's attention only when the most recent message
    # on it was posted by someone else (staff) — not when the client is the
    # one waiting on a reply.
    open_tickets = account.tickets.exclude(
        status=SupportTicket.STATUS_RESOLVED,
    ).prefetch_related('messages')
    awaiting_reply = 0
    for ticket in open_tickets:
        messages = list(ticket.messages.all())
        if messages and messages[-1].sender_id != account.user_id:
            awaiting_reply += 1
    if awaiting_reply:
        items.append({
            'label': f"{awaiting_reply} ticket{'s' if awaiting_reply != 1 else ''} awaiting your reply",
            'href_name': 'clients:support',
            'tone': 'teal',
        })

    return items


def create_ticket(account, subject, body, sender):
    ticket = SupportTicket.objects.create(client_account=account, subject=subject)
    SupportMessage.objects.create(ticket=ticket, sender=sender, body=body)
    return ticket


def add_ticket_reply(ticket, body, sender):
    return SupportMessage.objects.create(ticket=ticket, sender=sender, body=body)
