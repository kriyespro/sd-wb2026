from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from projects.models import Meeting, Project, Report
from users.mixins import ClientPortalMixin, DashboardContextMixin
from users.services import get_dashboard_url_for_user

from .forms import SupportTicketForm, TicketReplyForm
from .models import SupportTicket
from .services import (
    CLIENT_NAV,
    add_ticket_reply,
    create_ticket,
    get_approved_deliverables,
    get_client_account,
    get_client_meetings,
    get_client_projects,
    get_client_reports,
    get_client_stats,
)


class ClientBaseMixin(DashboardContextMixin, ClientPortalMixin):
    portal_name = 'Client Portal'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['sidebar_links'] = CLIENT_NAV
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['account'] = get_client_account(self.request.user)
        return ctx


class ClientDashboardView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        account = ctx['account']
        ctx['page_title'] = 'Client Dashboard'
        ctx['stats'] = get_client_stats(account)
        ctx['recent_projects'] = get_client_projects(account)[:4]
        ctx['upcoming_meetings'] = get_client_meetings(account).filter(
            status=Meeting.STATUS_SCHEDULED,
        )[:3]
        return ctx


class ProjectsView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/projects.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Projects'
        ctx['projects'] = get_client_projects(ctx['account'])
        return ctx


class ProjectDetailView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/project_detail.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = get_object_or_404(
            get_client_projects(ctx['account']), pk=kwargs['pk'],
        )
        ctx['page_title'] = project.name
        ctx['project'] = project
        ctx['milestones'] = project.milestones.all()
        # Only approved deliverables are ever shown to the client.
        ctx['deliverables'] = project.deliverables.filter(
            approval_status='approved',
        )
        return ctx


class ReportsView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/reports.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Reports'
        ctx['reports'] = get_client_reports(ctx['account']).prefetch_related('metrics')
        return ctx


class FilesView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/files.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Files'
        ctx['deliverables'] = get_approved_deliverables(ctx['account'])
        return ctx


class MeetingsView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/meetings.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Meetings'
        ctx['meetings'] = get_client_meetings(ctx['account'])
        return ctx


class InvoicesView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/invoices.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Invoices'
        from billing.services import get_client_invoices

        ctx['invoices'] = get_client_invoices(ctx['account'])
        return ctx


class SupportView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/support.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Support'
        account = ctx['account']
        ctx['tickets'] = account.tickets.all() if account else []
        ctx['form'] = SupportTicketForm()
        return ctx


class SupportTicketCreateView(ClientPortalMixin, View):
    def post(self, request):
        account = get_client_account(request.user)
        form = SupportTicketForm(request.POST)
        if account and form.is_valid():
            create_ticket(
                account, form.cleaned_data['subject'], form.cleaned_data['body'], request.user,
            )
        return redirect('clients:support')


class SupportTicketDetailView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/ticket_detail.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        account = ctx['account']
        ticket = get_object_or_404(SupportTicket, pk=kwargs['pk'], client_account=account)
        ctx['page_title'] = ticket.subject
        ctx['ticket'] = ticket
        ctx['messages_list'] = ticket.messages.select_related('sender')
        ctx['reply_form'] = TicketReplyForm()
        return ctx


class SupportTicketReplyView(ClientPortalMixin, View):
    def post(self, request, pk):
        account = get_client_account(request.user)
        ticket = get_object_or_404(SupportTicket, pk=pk, client_account=account)
        form = TicketReplyForm(request.POST)
        if form.is_valid():
            add_ticket_reply(ticket, form.cleaned_data['body'], request.user)
        return redirect('clients:ticket_detail', pk=pk)


class AnalyticsView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/analytics.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Analytics'
        account = ctx['account']
        reports = get_client_reports(account).prefetch_related('metrics')
        metrics = []
        for report in reports:
            metrics.extend(report.metrics.all())
        ctx['metrics'] = metrics[:8]
        return ctx


class GoalsView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/goals.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Goals'
        account = ctx['account']
        ctx['goals'] = account.goals.all() if account else []
        return ctx


class ROIView(ClientBaseMixin, TemplateView):
    template_name = 'pages/dashboard/client/roi.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'ROI'
        account = ctx['account']
        completed = get_client_projects(account).filter(status=Project.STATUS_COMPLETED).count()
        ctx['completed_projects'] = completed
        ctx['total_projects'] = get_client_projects(account).count()
        return ctx
