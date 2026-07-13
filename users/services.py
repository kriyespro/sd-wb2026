from django.db import transaction
from django.urls import reverse
from django.utils.crypto import get_random_string

from .roles import (
    CLIENT_ROLES,
    OPS_ROLES,
    PARTNER_ROLES,
    PORTAL_CLIENT,
    PORTAL_OPS,
    PORTAL_PARTNER,
    PORTAL_STUDENT,
    PORTAL_URL_NAMES,
    ROLE_CLIENT_OWNER,
    ROLE_PARTNER,
    ROLE_STUDENT,
    STUDENT_ROLES,
)

PUBLIC_SIGNUP_ROLES = {ROLE_CLIENT_OWNER, ROLE_STUDENT, ROLE_PARTNER}

PUBLIC_SIGNUP_CHOICES = [
    (ROLE_CLIENT_OWNER, 'Business / Client'),
    (ROLE_STUDENT, 'Student'),
    (ROLE_PARTNER, 'DGC Partner'),
]

SESSION_SIGNUP_ROLE = 'signup_role'
SESSION_NEEDS_ROLE = 'needs_role_choice'


def get_portal_for_role(role):
    if role in CLIENT_ROLES:
        return PORTAL_CLIENT
    if role in STUDENT_ROLES:
        return PORTAL_STUDENT
    if role in PARTNER_ROLES:
        return PORTAL_PARTNER
    if role in OPS_ROLES:
        return PORTAL_OPS
    return PORTAL_OPS


def get_dashboard_url_name_for_user(user):
    if not user.is_authenticated:
        return 'users:login'
    if not hasattr(user, 'profile'):
        return 'users:login'
    portal = get_portal_for_role(user.profile.role)
    return PORTAL_URL_NAMES[portal]


def get_dashboard_url_for_user(user):
    return reverse(get_dashboard_url_name_for_user(user))


def _unique_partner_code(name):
    from partners.models import PartnerProfile

    base = ''.join(ch for ch in (name or '').upper() if ch.isalnum())[:4] or 'DGC'
    for _ in range(20):
        code = f'{base}{get_random_string(4, allowed_chars="0123456789")}'
        if not PartnerProfile.objects.filter(code=code).exists():
            return code
    return f'DGC{get_random_string(6, allowed_chars="0123456789")}'


def _unique_username(email, name=''):
    from django.contrib.auth.models import User

    base = (email or '').split('@')[0][:20] or ''.join(
        ch for ch in (name or 'user').lower() if ch.isalnum()
    )[:20] or 'user'
    username = base
    n = 1
    while User.objects.filter(username=username).exists():
        username = f'{base}{n}'
        n += 1
    return username


@transaction.atomic
def provision_public_signup(user, role):
    """Assign a public signup role and create related portal records."""
    if role not in PUBLIC_SIGNUP_ROLES:
        raise ValueError('Role is not open for self-serve signup')

    from clients.models import ClientAccount
    from partners.models import PartnerProfile

    from .models import Profile

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = role
    profile.save(update_fields=['role'])
    # Keep reverse OneToOne cache in sync (login updates last_login and would
    # otherwise re-save a stale default role via the profile signal).
    user.profile = profile

    if role == ROLE_CLIENT_OWNER:
        if not ClientAccount.objects.filter(user=user).exists():
            company = (
                user.get_full_name().strip()
                or (user.email.split('@')[0] if user.email else user.username)
            )
            ClientAccount.objects.create(user=user, company_name=company[:200] or 'My Business')

    elif role == ROLE_PARTNER:
        if not PartnerProfile.objects.filter(user=user).exists():
            name = user.get_full_name() or user.username
            PartnerProfile.objects.create(user=user, code=_unique_partner_code(name))

    # student: role only
    return user


def create_public_user(*, email, password, role, first_name='', last_name='', phone=''):
    from django.contrib.auth.models import User

    if role not in PUBLIC_SIGNUP_ROLES:
        raise ValueError('Role is not open for self-serve signup')

    email = email.strip().lower()
    user = User.objects.create_user(
        username=_unique_username(email, first_name),
        email=email,
        password=password,
        first_name=(first_name or '')[:30],
        last_name=(last_name or '')[:30],
    )
    if phone:
        user.profile.phone = phone
        user.profile.save(update_fields=['phone'])
    provision_public_signup(user, role)
    return user
