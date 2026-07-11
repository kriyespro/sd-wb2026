from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .roles import CLIENT_ROLES, OPS_ROLES, PARTNER_ROLES, STUDENT_ROLES
from .services import get_dashboard_url_for_user


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = set()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'profile'):
            return redirect('users:login')
        if self.allowed_roles and request.user.profile.role not in self.allowed_roles:
            return redirect(get_dashboard_url_for_user(request.user))
        return super().dispatch(request, *args, **kwargs)


class ClientPortalMixin(RoleRequiredMixin):
    allowed_roles = CLIENT_ROLES


class StudentPortalMixin(RoleRequiredMixin):
    allowed_roles = STUDENT_ROLES


class PartnerPortalMixin(RoleRequiredMixin):
    allowed_roles = PARTNER_ROLES


class OpsPortalMixin(RoleRequiredMixin):
    allowed_roles = OPS_ROLES


class DashboardContextMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        if 'modules' in ctx:
            ctx['sidebar_links'] = ctx['modules']
        return ctx
