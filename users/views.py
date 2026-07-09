from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.views import View

from .forms import LoginForm
from .services import get_dashboard_url_for_user


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
    return redirect(get_dashboard_url_for_user(request.user))
