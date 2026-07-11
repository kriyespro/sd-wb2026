from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from academy.models import AdmissionApplication, MentorAllocation
from projects.models import Deliverable, Project
from users.mixins import DashboardContextMixin, OpsPortalMixin
from users.services import get_dashboard_url_for_user
from website.models import Lead

from .forms import LeadAssignForm, LeadConvertForm, LeadNotesForm, LeadStatusForm, MentorAllocationForm, ProjectAssignmentForm
from .lead_services import (
    assign_lead,
    convert_lead_to_client,
    get_sales_executives,
    save_handoff_notes,
    update_lead_status,
)
from .services import (
    OPS_NAV,
    approve_deliverable,
    get_mission_control_context,
    get_ops_stats,
    get_pending_deliverables,
    get_recent_leads,
    get_teams,
    reject_deliverable,
    validate_project_staffing,
)


class OpsBaseMixin(DashboardContextMixin, OpsPortalMixin):
    portal_name = 'Internal Ops'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['sidebar_links'] = OPS_NAV
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['dashboard_label'] = 'Mission Control'
        return ctx


class OpsDashboardView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mission Control'
        ctx.update(get_mission_control_context())
        return ctx


class OpsMissionLiveView(OpsPortalMixin, View):
    """HTMX poll endpoint — returns OOB fragments for mission control panels."""

    def get(self, request):
        return render(
            request,
            'partials/ops/_mission_live.jinja',
            get_mission_control_context(),
        )


class OpsLeadsLiveView(OpsPortalMixin, View):
    """HTMX poll endpoint — refreshes the full leads list on /ops/leads/."""

    def get(self, request):
        return render(request, 'partials/ops/_leads_list.jinja', _leads_list_context())


class QualityCheckView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/quality_check.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Quality Check'
        ctx['deliverables'] = get_pending_deliverables()
        return ctx


class DeliverableApproveView(OpsPortalMixin, View):
    def post(self, request, pk):
        deliverable = get_object_or_404(Deliverable, pk=pk)
        approve_deliverable(deliverable, request.user)
        return render(request, 'partials/_deliverable_row.jinja', {
            'deliverable': deliverable,
            'done_label': 'Approved — now client-visible',
        })


class DeliverableRejectView(OpsPortalMixin, View):
    def post(self, request, pk):
        deliverable = get_object_or_404(Deliverable, pk=pk)
        reject_deliverable(deliverable, request.user)
        return render(request, 'partials/_deliverable_row.jinja', {
            'deliverable': deliverable,
            'done_label': 'Rejected — hidden from client',
        })


class OpsProjectsView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/projects.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Projects'
        projects = Project.objects.select_related('client_account', 'project_manager').prefetch_related('assignments')
        rows = []
        for project in projects:
            rows.append({'project': project, 'issues': validate_project_staffing(project)})
        ctx['project_rows'] = rows
        return ctx


class PipelineView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/pipeline.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Talent Pipeline'
        apps = AdmissionApplication.objects.all()
        ctx['stages'] = [
            {'label': 'New', 'applications': apps.filter(status=AdmissionApplication.STATUS_NEW)},
            {'label': 'Under Review', 'applications': apps.filter(status=AdmissionApplication.STATUS_REVIEW)},
            {'label': 'Accepted', 'applications': apps.filter(status=AdmissionApplication.STATUS_ACCEPTED)},
            {'label': 'Rejected', 'applications': apps.filter(status=AdmissionApplication.STATUS_REJECTED)},
        ]
        return ctx


class AllocationView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/allocation.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Project Allocation'
        ctx['form'] = ProjectAssignmentForm()
        projects = Project.objects.prefetch_related('assignments__user')
        rows = []
        for project in projects:
            rows.append({
                'project': project,
                'assignments': project.assignments.all(),
                'issues': validate_project_staffing(project),
            })
        ctx['project_rows'] = rows
        return ctx


class AllocationCreateView(OpsPortalMixin, View):
    def post(self, request):
        form = ProjectAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('operations:allocation')


class MentorsView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/mentors.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mentor Allocation'
        ctx['form'] = MentorAllocationForm()
        ctx['allocations'] = MentorAllocation.objects.select_related('student', 'mentor')
        return ctx


class MentorAllocateView(OpsPortalMixin, View):
    def post(self, request):
        form = MentorAllocationForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            MentorAllocation.objects.update_or_create(
                student=student,
                defaults={
                    'mentor': form.cleaned_data['mentor'],
                    'notes': form.cleaned_data['notes'],
                },
            )
        return redirect('operations:mentors')


class TeamView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/team.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Team'
        ctx['teams'] = get_teams()
        return ctx


class PerformanceView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/performance.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Performance'
        from .models import PerformanceReview
        ctx['reviews'] = PerformanceReview.objects.select_related('user', 'reviewer')
        return ctx


def _lead_row_context(lead):
    return {
        'lead': lead,
        'status_choices': Lead.STATUS_CHOICES,
        'sales_executives': get_sales_executives(),
    }


def _leads_list_context():
    return {
        'leads': get_recent_leads(100),
        'status_choices': Lead.STATUS_CHOICES,
        'status_counts': {
            status: Lead.objects.filter(status=status).count()
            for status, _ in Lead.STATUS_CHOICES
        },
        'sales_executives': get_sales_executives(),
    }


class LeadsView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/leads.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Leads'
        ctx.update(_leads_list_context())
        return ctx


class LeadStatusUpdateView(OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadStatusForm(request.POST)
        if form.is_valid():
            update_lead_status(lead, form.cleaned_data['status'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadAssignView(OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadAssignForm(request.POST)
        if form.is_valid():
            assign_lead(lead, form.cleaned_data['assigned_to'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadNotesUpdateView(OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadNotesForm(request.POST)
        if form.is_valid():
            save_handoff_notes(lead, form.cleaned_data['handoff_notes'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadConvertView(OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadConvertForm(request.POST)
        if form.is_valid() and not lead.is_converted:
            try:
                convert_lead_to_client(
                    lead,
                    project_name=form.cleaned_data['project_name'],
                    account_manager=lead.assigned_to,
                )
            except ValueError:
                pass
        lead.refresh_from_db()
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class OpsInvoicesView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/invoices.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Invoices'
        from billing.services import get_all_invoices

        ctx['invoices'] = get_all_invoices()
        return ctx
