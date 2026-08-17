from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from users.mixins import DashboardContextMixin
from users.roles import PORTAL_CLIENT, PORTAL_OPS, PORTAL_PARTNER, PORTAL_STUDENT
from users.services import get_dashboard_url_for_user, get_portal_for_role

from .services import articles_for_user

KNOWLEDGE_LINK = {'title': 'Knowledge Base', 'icon': '📚', 'url_name': 'knowledge:index'}


def _portal_nav(user):
    """The Knowledge Base is reachable from every portal, so its own page
    must keep showing that portal's full menu (not a stripped-down one-item
    list) — otherwise navigating here strands the user with no way back to
    the rest of their dashboard except the browser back button."""
    if not hasattr(user, 'profile'):
        return [KNOWLEDGE_LINK]
    portal = get_portal_for_role(user.profile.role)
    if portal == PORTAL_CLIENT:
        from clients.services import CLIENT_NAV
        return CLIENT_NAV
    if portal == PORTAL_STUDENT:
        from academy.services import STUDENT_NAV
        return STUDENT_NAV
    if portal == PORTAL_PARTNER:
        from partners.services import DGC_NAV
        return DGC_NAV
    if portal == PORTAL_OPS:
        from operations.services import OPS_NAV
        return OPS_NAV
    return [KNOWLEDGE_LINK]


class KnowledgeBaseMixin(LoginRequiredMixin, DashboardContextMixin):
    portal_name = 'Knowledge Base'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['dashboard_label'] = 'Home'
        ctx['sidebar_links'] = _portal_nav(self.request.user)
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
