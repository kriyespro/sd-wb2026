from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services import (
    PUBLIC_SIGNUP_ROLES,
    SESSION_SIGNUP_ROLE,
    get_dashboard_url_for_user,
    needs_role_choice,
    provision_public_signup,
)


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Public signup is Google-only via social adapter.
        return False

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            if needs_role_choice(request.user):
                from django.urls import reverse
                return reverse('users:choose_role')
            return get_dashboard_url_for_user(request.user)
        return super().get_login_redirect_url(request)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        # Google already verified the email — mark it verified locally.
        if user.email:
            EmailAddress.objects.update_or_create(
                user=user,
                email=user.email.lower(),
                defaults={'verified': True, 'primary': True},
            )
        role = request.session.pop(SESSION_SIGNUP_ROLE, None)
        if role in PUBLIC_SIGNUP_ROLES:
            provision_public_signup(user, role)
        else:
            # Persisted on the profile (not just the session) so a lost/expired
            # session can't leave this account stuck on the default role with
            # real portal access — see users/models.py Profile.role_confirmed.
            user.profile.role_confirmed = False
            user.profile.save(update_fields=['role_confirmed'])
        return user

    def pre_social_login(self, request, sociallogin):
        """Existing accounts skip role selection; still ensure email is verified."""
        if sociallogin.is_existing:
            request.session.pop(SESSION_SIGNUP_ROLE, None)
            user = sociallogin.user
            if user and user.email:
                EmailAddress.objects.update_or_create(
                    user=user,
                    email=user.email.lower(),
                    defaults={'verified': True, 'primary': True},
                )
