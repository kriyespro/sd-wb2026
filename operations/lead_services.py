from django.contrib.auth.models import User
from django.db import transaction
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from clients.models import ClientAccount
from projects.models import Project
from users.models import Profile
from users.roles import OFFICE_DESK_ROLES, ROLE_CLIENT_OWNER
from website.models import Lead
from website.services import ensure_lead_followups


def get_sales_executives():
    """Legacy alias — office desk assignees."""
    return get_office_desk_users()


def get_office_desk_users():
    return User.objects.filter(
        profile__role__in=OFFICE_DESK_ROLES,
        is_active=True,
    ).select_related('profile').order_by('first_name', 'username')


def set_next_follow_up(lead, when):
    lead.next_follow_up_at = when
    lead.save(update_fields=['next_follow_up_at', 'updated_at'])
    return lead


def update_lead_status(lead, status):
    lead.status = status
    lead.save(update_fields=['status', 'updated_at'])
    return lead


def assign_lead(lead, user):
    lead.assigned_to = user
    lead.save(update_fields=['assigned_to', 'updated_at'])
    ensure_lead_followups(lead)
    return lead


def save_handoff_notes(lead, notes):
    lead.handoff_notes = notes
    lead.save(update_fields=['handoff_notes', 'updated_at'])
    return lead


def _unique_username(email, name):
    base = slugify(email.split('@')[0]) or slugify(name) or 'client'
    base = base[:30]
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f'{base}{counter}'[:30]
        counter += 1
    return username


@transaction.atomic
def convert_lead_to_client(lead, project_name='', account_manager=None):
    if lead.is_converted:
        raise ValueError('Lead is already converted.')

    existing = User.objects.filter(email__iexact=lead.email).first()
    if existing:
        user = existing
        profile, _ = Profile.objects.get_or_create(user=user)
        if profile.role not in {ROLE_CLIENT_OWNER}:
            profile.role = ROLE_CLIENT_OWNER
            profile.save(update_fields=['role'])
        account = getattr(user, 'client_account', None)
        if not account:
            account = ClientAccount.objects.create(
                user=user,
                company_name=lead.company or lead.name,
                industry='',
                account_manager=account_manager or lead.assigned_to,
            )
    else:
        user = User.objects.create_user(
            username=_unique_username(lead.email, lead.name),
            email=lead.email,
            first_name=lead.name.split()[0] if lead.name else '',
            last_name=' '.join(lead.name.split()[1:]) if lead.name and ' ' in lead.name else '',
            password=get_random_string(12),
        )
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = ROLE_CLIENT_OWNER
        profile.save(update_fields=['role'])
        account = ClientAccount.objects.create(
            user=user,
            company_name=lead.company or lead.name,
            industry='',
            account_manager=account_manager or lead.assigned_to,
        )

    project_title = project_name or f'{lead.service_interest or "Growth"} — {account.company_name}'
    project = Project.objects.create(
        client_account=account,
        name=project_title[:200],
        service_type=lead.service_interest or '',
        description=lead.message or '',
        status=Project.STATUS_PLANNING,
        project_manager=account_manager,
    )

    lead.status = Lead.STATUS_WON
    lead.converted_client = account
    lead.save(update_fields=['status', 'converted_client', 'updated_at'])

    return account, project, user
