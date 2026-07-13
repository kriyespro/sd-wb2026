from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services import (
    PUBLIC_SIGNUP_ROLES,
    SESSION_NEEDS_ROLE,
    SESSION_SIGNUP_ROLE,
    get_dashboard_url_for_user,
    provision_public_signup,
)


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.session.get(SESSION_NEEDS_ROLE):
            from django.urls import reverse
            return reverse('users:choose_role')
        if request.user.is_authenticated:
            return get_dashboard_url_for_user(request.user)
        return super().get_login_redirect_url(request)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        role = request.session.pop(SESSION_SIGNUP_ROLE, None)
        if role in PUBLIC_SIGNUP_ROLES:
            provision_public_signup(user, role)
            request.session.pop(SESSION_NEEDS_ROLE, None)
        else:
            request.session[SESSION_NEEDS_ROLE] = True
        return user

    def pre_social_login(self, request, sociallogin):
        """Existing accounts skip role selection."""
        if sociallogin.is_existing:
            request.session.pop(SESSION_NEEDS_ROLE, None)
            request.session.pop(SESSION_SIGNUP_ROLE, None)
