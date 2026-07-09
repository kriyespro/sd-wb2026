from django.shortcuts import redirect

from .roles import CLIENT_ROLES, OPS_ROLES, PORTAL_PATHS, STUDENT_ROLES
from .services import get_dashboard_url_for_user


PORTAL_RULES = (
    ('/dashboard/client/', CLIENT_ROLES),
    ('/dashboard/student/', STUDENT_ROLES),
    ('/ops/', OPS_ROLES),
)


class PortalAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            path = request.path
            role = request.user.profile.role
            for prefix, allowed_roles in PORTAL_RULES:
                if path.startswith(prefix) and role not in allowed_roles:
                    return redirect(get_dashboard_url_for_user(request.user))
        return self.get_response(request)
