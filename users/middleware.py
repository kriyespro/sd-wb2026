from django.shortcuts import redirect

from .roles import CLIENT_ROLES, OPS_ROLES, PARTNER_ROLES, STUDENT_ROLES
from .services import get_dashboard_url_for_user


PORTAL_RULES = (
    ('/dashboard/client/', CLIENT_ROLES),
    ('/dashboard/student/', STUDENT_ROLES),
    ('/dashboard/dgc/', PARTNER_ROLES),
    ('/ops/', OPS_ROLES),
    ('/ops2/', OPS_ROLES),
)

DGC_PROFILE_PREFIX = '/dashboard/dgc/profile'
FORCE_PASSWORD_CHANGE_PATH = '/auth/force-password-change/'


class PortalAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            path = request.path
            role = request.user.profile.role

            # Legacy DGC accounts with an outstanding temp password must
            # change it before touching any portal (except the change form
            # itself / logout).
            partner = getattr(request.user, 'partner_profile', None)
            if (
                partner and partner.must_change_password
                and path != FORCE_PASSWORD_CHANGE_PATH
                and not path.startswith('/auth/logout')
            ):
                return redirect('users:force_password_change')

            for prefix, allowed_roles in PORTAL_RULES:
                if path.startswith(prefix) and role not in allowed_roles:
                    return redirect(get_dashboard_url_for_user(request.user))

            # Pending DGC partners may only use the KYC / profile page
            if path.startswith('/dashboard/dgc/') and role in PARTNER_ROLES:
                from partners.services import partner_is_approved
                if not partner_is_approved(request.user) and not path.startswith(DGC_PROFILE_PREFIX):
                    return redirect('partners:profile')
        return self.get_response(request)
