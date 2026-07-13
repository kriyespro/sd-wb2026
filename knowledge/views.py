from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from users.mixins import DashboardContextMixin
from users.services import get_dashboard_url_for_user

from .services import articles_for_user


class KnowledgeBaseMixin(LoginRequiredMixin, DashboardContextMixin):
    portal_name = 'Knowledge Base'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['dashboard_label'] = 'Home'
        ctx['sidebar_links'] = [
            {'title': 'All articles', 'icon': '📚', 'url_name': 'knowledge:index'},
        ]
        return ctx


class KnowledgeIndexView(KnowledgeBaseMixin, TemplateView):
    template_name = 'pages/knowledge/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        articles = articles_for_user(self.request.user)
        ctx['page_title'] = 'Knowledge Base'
        ctx['articles'] = articles
        ctx['categories'] = sorted({
            a.category for a in articles if a.category
        })
        return ctx


class KnowledgeDetailView(KnowledgeBaseMixin, DetailView):
    template_name = 'pages/knowledge/detail.jinja'
    context_object_name = 'article'

    def get_queryset(self):
        return articles_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = self.object.title
        return ctx
