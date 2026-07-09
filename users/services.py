from django.urls import reverse

from .roles import (
    CLIENT_ROLES,
    OPS_ROLES,
    PORTAL_CLIENT,
    PORTAL_OPS,
    PORTAL_STUDENT,
    PORTAL_URL_NAMES,
    STUDENT_ROLES,
)


def get_portal_for_role(role):
    if role in CLIENT_ROLES:
        return PORTAL_CLIENT
    if role in STUDENT_ROLES:
        return PORTAL_STUDENT
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
