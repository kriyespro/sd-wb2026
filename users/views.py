from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import ChooseRoleForm, LoginForm
from .services import (
    PUBLIC_SIGNUP_CHOICES,
    PUBLIC_SIGNUP_ROLES,
    SESSION_SIGNUP_ROLE,
    get_dashboard_url_for_user,
    needs_role_choice,
    provision_public_signup,
)


class LoginView(AuthLoginView):
    template_name = 'pages/auth/login.jinja'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return get_dashboard_url_for_user(self.request.user)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('website:home')

    def post(self, request):
        logout(request)
        return redirect('website:home')


def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    if needs_role_choice(request.user):
        return redirect('users:choose_role')
    return redirect(get_dashboard_url_for_user(request.user))


@require_http_methods(['GET', 'POST'])
def signup(request):
    """Google-only signup: pick a public role, then continue with Google."""
    if request.user.is_authenticated and not needs_role_choice(request.user):
        return redirect(get_dashboard_url_for_user(request.user))

    selected_role = request.GET.get('role', '').strip()
    if request.method == 'POST':
        selected_role = request.POST.get('role', '').strip()

    if selected_role and selected_role not in PUBLIC_SIGNUP_ROLES:
        selected_role = ''

    # POST with a valid role → store session and start Google OAuth
    if request.method == 'POST' and selected_role:
        request.session[SESSION_SIGNUP_ROLE] = selected_role
        return redirect('/accounts/google/login/')

    return render(request, 'pages/auth/signup.jinja', {
        'page_title': 'Create account',
        'role_choices': PUBLIC_SIGNUP_CHOICES,
        'selected_role': selected_role,
        'error': 'Please choose how you are joining.' if request.method == 'POST' else '',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def choose_role(request):
    if not needs_role_choice(request.user):
        return redirect(get_dashboard_url_for_user(request.user))

    if request.method == 'POST':
        form = ChooseRoleForm(request.POST)
        if form.is_valid():
            provision_public_signup(request.user, form.cleaned_data['role'])
            return redirect(get_dashboard_url_for_user(request.user))
    else:
        form = ChooseRoleForm()

    return render(request, 'pages/auth/choose_role.jinja', {
        'form': form,
        'page_title': 'Choose how you join',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def force_password_change(request):
    """Legacy DGC accounts get a temp password at approval time; this gate
    (enforced by PortalAccessMiddleware) makes sure it can't be used as a
    standing credential."""
    partner = getattr(request.user, 'partner_profile', None)
    if not partner or not partner.must_change_password:
        return redirect(get_dashboard_url_for_user(request.user))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            partner.must_change_password = False
            partner.save(update_fields=['must_change_password'])
            from partners.models import DgcApplication
            DgcApplication.objects.filter(
                partner_user=request.user,
            ).exclude(temp_password='').update(temp_password='')
            return redirect(get_dashboard_url_for_user(request.user))
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'pages/auth/force_password_change.jinja', {
        'form': form,
        'page_title': 'Set your password',
    })


@require_http_methods(['GET'])
def google_start(request):
    """Store optional signup role, then start Google OAuth."""
    role = request.GET.get('role', '').strip()
    if role in PUBLIC_SIGNUP_ROLES:
        request.session[SESSION_SIGNUP_ROLE] = role
    else:
        request.session.pop(SESSION_SIGNUP_ROLE, None)
    return redirect('/accounts/google/login/')
