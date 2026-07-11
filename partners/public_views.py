from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .forms import DgcApplicationForm
from .services import create_dgc_application


class DgcLandingView(TemplateView):
    template_name = 'pages/dgc/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Join as DGC'
        ctx['meta_description'] = (
            'Become a Digital Growth Consultant (DGC) — marketing partner for '
            'Winning Blueprints. Earn commission on reseller offers and factory leads.'
        )
        ctx['form'] = DgcApplicationForm()
        return ctx


class DgcApplyView(View):
    def get(self, request):
        return redirect('partners_public:landing')

    def post(self, request):
        form = DgcApplicationForm(request.POST)
        if form.is_valid():
            create_dgc_application(form)
            if request.headers.get('HX-Request'):
                return render(request, 'partials/dgc/_apply_success.jinja')
            return render(request, 'pages/dgc/index.jinja', {
                'page_title': 'Join as DGC',
                'form': DgcApplicationForm(),
                'submitted': True,
            })
        if request.headers.get('HX-Request'):
            return render(request, 'partials/dgc/_apply_form.jinja', {
                'form': form,
                'show_errors': True,
            })
        return render(request, 'pages/dgc/index.jinja', {
            'page_title': 'Join as DGC',
            'form': form,
            'show_errors': True,
        }, status=400)
