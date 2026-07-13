from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import ChooseRoleForm, LoginForm, PublicSignupForm
from .services import (
    PUBLIC_SIGNUP_ROLES,
    SESSION_NEEDS_ROLE,
    SESSION_SIGNUP_ROLE,
    get_dashboard_url_for_user,
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
    if request.session.get(SESSION_NEEDS_ROLE):
        return redirect('users:choose_role')
    return redirect(get_dashboard_url_for_user(request.user))


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated and not request.session.get(SESSION_NEEDS_ROLE):
        return redirect(get_dashboard_url_for_user(request.user))

    initial_role = request.GET.get('role', '').strip()
    if initial_role not in PUBLIC_SIGNUP_ROLES:
        initial_role = ''

    if request.method == 'POST':
        form = PublicSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.pop(SESSION_NEEDS_ROLE, None)
            request.session.pop(SESSION_SIGNUP_ROLE, None)
            return redirect(get_dashboard_url_for_user(user))
    else:
        form = PublicSignupForm(initial={'role': initial_role} if initial_role else None)

    return render(request, 'pages/auth/signup.jinja', {
        'form': form,
        'page_title': 'Create account',
        'selected_role': initial_role or (form.data.get('role') if form.is_bound else ''),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def choose_role(request):
    if not request.session.get(SESSION_NEEDS_ROLE):
        return redirect(get_dashboard_url_for_user(request.user))

    if request.method == 'POST':
        form = ChooseRoleForm(request.POST)
        if form.is_valid():
            provision_public_signup(request.user, form.cleaned_data['role'])
            request.session.pop(SESSION_NEEDS_ROLE, None)
            return redirect(get_dashboard_url_for_user(request.user))
    else:
        form = ChooseRoleForm()

    return render(request, 'pages/auth/choose_role.jinja', {
        'form': form,
        'page_title': 'Choose how you join',
    })


@require_http_methods(['GET'])
def google_start(request):
    """Store optional signup role, then start Google OAuth."""
    role = request.GET.get('role', '').strip()
    if role in PUBLIC_SIGNUP_ROLES:
        request.session[SESSION_SIGNUP_ROLE] = role
        request.session.pop(SESSION_NEEDS_ROLE, None)
    else:
        request.session.pop(SESSION_SIGNUP_ROLE, None)
    return redirect('/accounts/google/login/')
