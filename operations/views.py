from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from academy.models import AdmissionApplication, MentorAllocation
from projects.models import Deliverable, Project
from users.mixins import DashboardContextMixin, OpsPortalMixin
from users.roles import ROLE_SUPER_ADMIN
from users.services import get_dashboard_url_for_user
from partners.models import DgcApplication, PartnerLead
from partners.services import approve_dgc_application, update_lead_status
from website.models import JobApplication, Lead

from .forms import (
    JobApplicationStatusForm,
    LeadAssignForm,
    LeadConvertForm,
    LeadNotesForm,
    LeadStatusForm,
    MentorAllocationForm,
    ProjectAssignmentForm,
)
from .lead_services import (
    assign_lead,
    convert_lead_to_client,
    get_sales_executives,
    save_handoff_notes,
    update_lead_status,
)
from .services import (
    OPS_NAV,
    OPS_NAV_SUPERUSER,
    approve_deliverable,
    get_mission_control_context,
    get_ops_stats,
    get_pending_deliverables,
    get_recent_leads,
    get_teams,
    reject_deliverable,
    validate_project_staffing,
)


def _is_superuser(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or getattr(getattr(user, 'profile', None), 'role', None) == ROLE_SUPER_ADMIN
        )
    )


class SuperAdminRequiredMixin(OpsPortalMixin):
    """Ops pages restricted to Django superuser or Super Admin role."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not _is_superuser(request.user):
            return redirect(get_dashboard_url_for_user(request.user))
        return super().dispatch(request, *args, **kwargs)


class OpsBaseMixin(DashboardContextMixin, OpsPortalMixin):
    portal_name = 'Internal Ops'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        nav = list(OPS_NAV)
        if _is_superuser(self.request.user):
            nav = nav + list(OPS_NAV_SUPERUSER)
        ctx['sidebar_links'] = nav
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['dashboard_label'] = 'Mission Control'
        ctx['is_superuser_ops'] = _is_superuser(self.request.user)
        return ctx


class OpsDashboardView(OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mission Control'
        include_jobs = ctx.get('is_superuser_ops', False)
        ctx.update(get_mission_control_context(include_jobs=include_jobs))
        return ctx


class OpsMissionLiveView(OpsPortalMixin, View):
    """HTMX poll endpoint — returns OOB fragments for mission control panels."""

    def get(self, request):
        include_jobs = _is_superuser(request.user)
        ctx = get_mission_control_context(include_jobs=include_jobs)
        ctx['is_superuser_ops'] = include_jobs
        return render(request, 'partials/ops/_mission_live.jinja', ctx)


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


class JobApplicationsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/job_applications.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        applications = JobApplication.objects.all()
        ctx['page_title'] = 'Job Applications'
        ctx['applications'] = applications
        ctx['status_choices'] = JobApplication.STATUS_CHOICES
        ctx['status_counts'] = {
            status: applications.filter(status=status).count()
            for status, _ in JobApplication.STATUS_CHOICES
        }
        ctx['total_count'] = applications.count()
        return ctx


class JobApplicationStatusUpdateView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        form = JobApplicationStatusForm(request.POST)
        if form.is_valid():
            application.status = form.cleaned_data['status']
            application.save(update_fields=['status'])
        return render(request, 'partials/ops/_job_application_row.jinja', {
            'app': application,
            'status_choices': JobApplication.STATUS_CHOICES,
        })


class DgcApplicationsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/dgc_applications.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        applications = DgcApplication.objects.all()
        ctx['page_title'] = 'DGC Applications'
        ctx['applications'] = applications
        ctx['status_choices'] = DgcApplication.STATUS_CHOICES
        ctx['status_counts'] = {
            status: applications.filter(status=status).count()
            for status, _ in DgcApplication.STATUS_CHOICES
        }
        ctx['total_count'] = applications.count()
        return ctx


class DgcApplicationApproveView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        try:
            user, temp_password = approve_dgc_application(application, request.user)
            messages.success(
                request,
                f'Approved {application.name}. Login: {user.username} / temp password: {temp_password}',
            )
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('operations:dgc_applications')


class DgcApplicationRejectView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        if application.status != DgcApplication.STATUS_APPROVED:
            application.status = DgcApplication.STATUS_REJECTED
            application.reviewed_by = request.user
            application.save(update_fields=['status', 'reviewed_by', 'updated_at'])
            messages.success(request, f'Rejected {application.name}.')
        else:
            messages.error(request, 'Already approved — cannot reject.')
        return redirect('operations:dgc_applications')


class DgcLeadsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/dgc_leads.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leads = PartnerLead.objects.select_related(
            'partner', 'partner__user',
        ).all()
        ctx['page_title'] = 'DGC Leads'
        ctx['leads'] = leads
        ctx['status_choices'] = PartnerLead.STATUS_CHOICES
        ctx['status_counts'] = {
            status: leads.filter(status=status).count()
            for status, _ in PartnerLead.STATUS_CHOICES
        }
        ctx['total_count'] = leads.count()
        return ctx


class DgcLeadStatusUpdateView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(
            PartnerLead.objects.select_related('partner', 'partner__user'),
            pk=pk,
        )
        status = request.POST.get('status')
        valid = {value for value, _ in PartnerLead.STATUS_CHOICES}
        if status in valid:
            update_lead_status(lead, status)
            lead.refresh_from_db()
        return render(request, 'partials/ops/_dgc_lead_row.jinja', {
            'lead': lead,
            'status_choices': PartnerLead.STATUS_CHOICES,
        })
