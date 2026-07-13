from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .roles import (
    CLIENT_ROLES,
    OPS_ROLES,
    PARTNER_ROLES,
    ROLE_SUPER_ADMIN,
    STUDENT_ROLES,
)
from .services import get_dashboard_url_for_user, needs_role_choice


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = set()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'profile'):
            return redirect('users:login')
        # An unconfirmed profile still carries the default client_owner role,
        # so this must be checked before allowed_roles or a lost/expired
        # signup session could grant a portal it was never provisioned for.
        if needs_role_choice(request.user):
            return redirect('users:choose_role')
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


class NarrowerOpsRoleMixin:
    """Layer on top of OpsPortalMixin to restrict a specific ops view to a
    subset of OPS_ROLES, while always letting Django superusers / Super Admin
    through. Put this mixin BEFORE the OpsPortalMixin/OpsBaseMixin in the
    subclass's bases so its dispatch runs first: it only narrows, it never
    widens — the underlying OpsPortalMixin.dispatch still enforces login +
    OPS_ROLES membership.
    """
    extra_allowed_roles = frozenset()

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and hasattr(user, 'profile'):
            role = user.profile.role
            is_super = user.is_superuser or role == ROLE_SUPER_ADMIN
            if not is_super and role not in self.extra_allowed_roles:
                return redirect(get_dashboard_url_for_user(user))
        return super().dispatch(request, *args, **kwargs)


class DashboardContextMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        if 'modules' in ctx:
            ctx['sidebar_links'] = ctx['modules']
        return ctx
