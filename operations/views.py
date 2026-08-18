from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from academy import fourd_services
from academy.forms import TeachingEvaluationForm
from academy.models import AdmissionApplication, MentorAllocation, TeachingSession
from academy.services import evaluate_teaching_session, get_student_stats
from core.pagination import paginate
from projects.models import Deliverable, Project
from users.mixins import DashboardContextMixin, NarrowerOpsRoleMixin, OpsPortalMixin
from users.services import get_dashboard_url_for_user
from partners.models import DgcApplication, PartnerLead, PartnerOrder
from partners.services import (
    approve_dgc_application,
    assign_order,
    cancel_dgc_application,
    pause_dgc_application,
    resume_dgc_application,
    update_lead_status as update_partner_lead_status,
    update_order_status,
)
from users.roles import (
    DELIVERY_ROLES,
    OFFICE_DESK_ROLES,
    ROLE_ACADEMY_ADMIN,
    ROLE_DIRECTOR,
    ROLE_MENTOR,
    ROLE_OFFICE,
    ROLE_PLACEMENT,
    ROLE_PM,
    ROLE_QA,
    ROLE_SUPER_ADMIN,
    ROLE_TRAINER,
    STUDENT_ROLES,
)
from website.forms import JobOpeningForm
from website.models import JobApplication, JobOpening, Lead, LeadFollowUp
from website.services import ensure_lead_followups, ensure_lead_followups_bulk, toggle_lead_followup

from .forms import (
    JobApplicationStatusForm,
    LeadAssignForm,
    LeadConvertForm,
    LeadNotesForm,
    LeadStatusForm,
    MentorAllocationForm,
    OrderAssignForm,
    ProjectAssignmentForm,
)
from .lead_services import (
    assign_lead,
    convert_lead_to_client,
    get_office_desk_users,
    get_sales_executives,
    save_handoff_notes,
    set_next_follow_up,
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
    status_counts_for,
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


class OfficeDeskRequiredMixin(NarrowerOpsRoleMixin):
    """Leads belong to sales/office/account-management desk roles — any other
    ops role (mentor, freelancer, qa_specialist, ...) could otherwise view,
    reassign and even convert leads into paying-client accounts."""
    extra_allowed_roles = OFFICE_DESK_ROLES | {ROLE_DIRECTOR}


class AllocationRequiredMixin(NarrowerOpsRoleMixin):
    """Project staffing decisions restricted to roles that actually manage
    delivery capacity, so any ops role can't assign themselves as PM."""
    extra_allowed_roles = {ROLE_PM, ROLE_OFFICE, ROLE_DIRECTOR}


class MentorAllocationRequiredMixin(NarrowerOpsRoleMixin):
    """Mentor assignment restricted to academy leadership roles."""
    extra_allowed_roles = {ROLE_ACADEMY_ADMIN, ROLE_PLACEMENT, ROLE_DIRECTOR}


class QaRequiredMixin(NarrowerOpsRoleMixin):
    """Deliverable approve/reject restricted to QA + management roles, so a
    delivery role (web_developer, content_writer, freelancer, ...) can't
    self-approve their own work straight to client-visible status."""
    extra_allowed_roles = {ROLE_QA, ROLE_PM, ROLE_OFFICE, ROLE_DIRECTOR}


class AcademyStaffRequiredMixin(NarrowerOpsRoleMixin):
    """Grading a student's teaching session, and viewing per-student 4D
    scores/mentor pairings, restricted to academy leadership and
    mentors/trainers who actually run the training — any other ops role
    (freelancer, seo_specialist, ...) has no business reading a student's
    individual progress or evaluation data."""
    extra_allowed_roles = {ROLE_MENTOR, ROLE_TRAINER, ROLE_ACADEMY_ADMIN, ROLE_DIRECTOR}


class ManagementRequiredMixin(NarrowerOpsRoleMixin):
    """Confidential staff performance reviews restricted to management —
    any ops role (freelancer, content_writer, ...) could otherwise browse
    every colleague's ratings and notes."""
    extra_allowed_roles = {ROLE_DIRECTOR, ROLE_OFFICE, ROLE_PM}


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


class OpsLeadsLiveView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
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


class DeliverableApproveView(QaRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        deliverable = get_object_or_404(Deliverable, pk=pk)
        approve_deliverable(deliverable, request.user)
        return render(request, 'partials/_deliverable_row.jinja', {
            'deliverable': deliverable,
            'done_label': 'Approved — now client-visible',
        })


class DeliverableRejectView(QaRequiredMixin, OpsPortalMixin, View):
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


class AllocationCreateView(AllocationRequiredMixin, OpsPortalMixin, View):
    def post(self, request):
        form = ProjectAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('operations:allocation')


class MentorsView(AcademyStaffRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/mentors.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mentor Allocation'
        ctx['form'] = MentorAllocationForm()
        ctx['allocations'] = MentorAllocation.objects.select_related('student', 'mentor')
        return ctx


class MentorAllocateView(MentorAllocationRequiredMixin, OpsPortalMixin, View):
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


class PerformanceView(ManagementRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/performance.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Performance'
        from .models import PerformanceReview
        ctx['reviews'] = PerformanceReview.objects.select_related('user', 'reviewer')
        return ctx


class Academy4DDashboardView(AcademyStaffRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/academy_4d.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = '4D Academy'
        ctx['batch_health'] = fourd_services.get_batch_health()
        leaderboard = fourd_services.get_leaderboard()
        ctx['leaderboard'] = leaderboard
        ctx['at_risk'] = [row for row in leaderboard if row['avg_score'] < 50]
        ctx['pending_evaluations'] = fourd_services.pending_teaching_evaluations()
        ctx['evaluation_form'] = TeachingEvaluationForm()
        return ctx


class TeachingEvaluateView(AcademyStaffRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        session = get_object_or_404(TeachingSession, pk=pk)
        form = TeachingEvaluationForm(request.POST)
        if form.is_valid():
            evaluate_teaching_session(
                session, request.user,
                form.cleaned_data['score'], form.cleaned_data['feedback'],
            )
        return redirect('operations:academy_4d')


class StudentProgressView(AcademyStaffRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/student_progress.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = get_object_or_404(User, pk=kwargs['pk'], profile__role__in=STUDENT_ROLES)
        ctx['page_title'] = f'Progress — {student.get_full_name() or student.username}'
        ctx['student'] = student
        ctx['daily_score'] = fourd_services.daily_score(student)
        ctx['score_level'] = fourd_services.score_level(ctx['daily_score'])
        ctx['score_history'] = fourd_services.get_score_history(student)
        ctx['activity_feed'] = fourd_services.get_activity_feed(student)
        ctx['pillar_totals'] = fourd_services.get_pillar_totals(student)
        ctx['streak'] = fourd_services.current_streak(student)
        ctx['student_stats'] = get_student_stats(student)
        return ctx


def _lead_row_context(lead):
    ensure_lead_followups(lead)
    return {
        'lead': lead,
        'status_choices': Lead.STATUS_CHOICES,
        'sales_executives': get_office_desk_users(),
        'followups': lead.followups.all(),
    }


def _leads_list_context():
    leads = list(get_recent_leads(100))
    ensure_lead_followups_bulk(leads)
    return {
        'leads': leads,
        'status_choices': Lead.STATUS_CHOICES,
        'status_counts': status_counts_for(Lead.objects.all(), Lead.STATUS_CHOICES),
        'sales_executives': get_office_desk_users(),
    }


class LeadsView(OfficeDeskRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/leads.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Leads'
        ctx.update(_leads_list_context())
        return ctx


class LeadStatusUpdateView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadStatusForm(request.POST)
        if form.is_valid():
            update_lead_status(lead, form.cleaned_data['status'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadAssignView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadAssignForm(request.POST)
        if form.is_valid():
            assign_lead(lead, form.cleaned_data['assigned_to'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadNotesUpdateView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadNotesForm(request.POST)
        if form.is_valid():
            save_handoff_notes(lead, form.cleaned_data['handoff_notes'])
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class LeadConvertView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
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


class LeadFollowUpToggleView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        followup = get_object_or_404(LeadFollowUp.objects.select_related('lead'), pk=pk)
        toggle_lead_followup(followup, request.user)
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(followup.lead))


class LeadNextFollowUpView(OfficeDeskRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        from datetime import datetime, time
        from django.utils.dateparse import parse_datetime, parse_date
        from django.utils import timezone as tz

        lead = get_object_or_404(Lead, pk=pk)
        raw = (request.POST.get('next_follow_up_at') or '').strip()
        when = None
        if raw:
            when = parse_datetime(raw)
            if when is None:
                d = parse_date(raw)
                if d:
                    when = tz.make_aware(datetime.combine(d, time(hour=10)))
            elif tz.is_naive(when):
                when = tz.make_aware(when)
        set_next_follow_up(lead, when)
        return render(request, 'partials/_lead_row.jinja', _lead_row_context(lead))


class FollowUpsView(OfficeDeskRequiredMixin, OpsBaseMixin, TemplateView):
    """Office desk — assigned enquiries + checklist progress."""

    template_name = 'pages/ops/follow_ups.jinja'

    def get_context_data(self, **kwargs):
        from django.utils import timezone as tz

        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Office Follow-ups'
        user = self.request.user
        open_statuses = [
            Lead.STATUS_NEW, Lead.STATUS_CONTACTED,
            Lead.STATUS_QUALIFIED, Lead.STATUS_PROPOSAL,
        ]
        mine = Lead.objects.filter(
            assigned_to=user, status__in=open_statuses,
        ).prefetch_related('followups')
        unassigned = Lead.objects.filter(
            assigned_to__isnull=True, status__in=open_statuses,
        ).prefetch_related('followups')[:20]
        due_soon = Lead.objects.filter(
            status__in=open_statuses,
            next_follow_up_at__lte=tz.now() + tz.timedelta(days=1),
            next_follow_up_at__isnull=False,
        ).select_related('assigned_to').prefetch_related('followups')[:20]
        mine, unassigned, due_soon = list(mine), list(unassigned), list(due_soon)
        ensure_lead_followups_bulk(mine + unassigned + due_soon)
        ctx['my_leads'] = mine
        ctx['unassigned_leads'] = unassigned
        ctx['due_soon'] = due_soon
        ctx['status_choices'] = Lead.STATUS_CHOICES
        ctx['sales_executives'] = get_office_desk_users()
        return ctx


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

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['partials/ops/_job_applications_panel.jinja']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_applications = JobApplication.objects.all()
        applications = all_applications

        status = self.request.GET.get('status', '').strip()
        application_type = self.request.GET.get('type', '').strip()
        role = self.request.GET.get('role', '').strip()
        q = self.request.GET.get('q', '').strip()

        if status:
            applications = applications.filter(status=status)
        else:
            # Rejected candidates stay out of the default view — still
            # reachable via the Rejected chip, not deleted.
            applications = applications.exclude(status=JobApplication.STATUS_REJECTED)
        if application_type:
            applications = applications.filter(application_type=application_type)
        if role:
            applications = applications.filter(role=role)
        if q:
            applications = applications.filter(
                Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q),
            )

        ctx['page_title'] = 'Job Applications'
        ctx['status_choices'] = JobApplication.STATUS_CHOICES
        ctx['type_choices'] = JobApplication.TYPE_CHOICES
        ctx['role_choices'] = list(
            all_applications.order_by('role').values_list('role', flat=True).distinct(),
        )
        ctx['status_counts'] = status_counts_for(all_applications, JobApplication.STATUS_CHOICES)
        ctx['total_count'] = all_applications.count()
        ctx['visible_total_count'] = all_applications.exclude(
            status=JobApplication.STATUS_REJECTED,
        ).count()
        ctx['filtered_count'] = applications.count()
        ctx['selected_status'] = status
        ctx['selected_type'] = application_type
        ctx['selected_role'] = role
        ctx['search_query'] = q
        ctx['has_filters'] = bool(status or application_type or role or q)

        page = paginate(self.request, applications)
        ctx['applications'] = page.object_list
        ctx['paginator_page'] = page

        params = self.request.GET.copy()
        params.pop('page', None)
        ctx['filter_querystring'] = ('&' + params.urlencode()) if params else ''
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


def _job_openings_context(form=None):
    return {
        'page_title': 'Job Openings',
        'form': form or JobOpeningForm(),
        'pending_openings': JobOpening.objects.filter(
            status=JobOpening.STATUS_PENDING,
        ).order_by('-created_at'),
        'openings': JobOpening.objects.filter(
            status=JobOpening.STATUS_APPROVED,
        ).order_by('-is_active', 'department', 'title'),
    }


class JobOpeningsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/job_openings.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_job_openings_context())
        return ctx


class JobOpeningCreateView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/job_openings.jinja'

    def post(self, request):
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('operations:job_openings')
        ctx = self.get_context_data()
        ctx.update(_job_openings_context(form=form))
        ctx['show_errors'] = True
        return self.render_to_response(ctx)


class JobOpeningEditView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/job_opening_edit.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        opening = get_object_or_404(JobOpening, pk=kwargs['pk'])
        ctx['page_title'] = f'Edit — {opening.title}'
        ctx['opening'] = opening
        ctx['form'] = ctx.get('form') or JobOpeningForm(instance=opening)
        return ctx

    def post(self, request, pk):
        opening = get_object_or_404(JobOpening, pk=pk)
        form = JobOpeningForm(request.POST, instance=opening)
        if form.is_valid():
            form.save()
            return redirect('operations:job_openings')
        ctx = self.get_context_data(pk=pk, form=form)
        ctx['show_errors'] = True
        return self.render_to_response(ctx)


class JobOpeningToggleView(SuperAdminRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        opening = get_object_or_404(JobOpening, pk=pk)
        opening.is_active = not opening.is_active
        opening.save(update_fields=['is_active'])
        return render(request, 'partials/ops/_job_opening_row.jinja', {'opening': opening})


class JobOpeningApproveView(SuperAdminRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        opening = get_object_or_404(JobOpening, pk=pk, status=JobOpening.STATUS_PENDING)
        opening.status = JobOpening.STATUS_APPROVED
        opening.is_active = True
        opening.save(update_fields=['status', 'is_active'])
        return HttpResponse('')


class JobOpeningRejectView(SuperAdminRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        opening = get_object_or_404(JobOpening, pk=pk, status=JobOpening.STATUS_PENDING)
        opening.status = JobOpening.STATUS_REJECTED
        opening.is_active = False
        opening.save(update_fields=['status', 'is_active'])
        return HttpResponse('')


class JobOpeningDeleteView(SuperAdminRequiredMixin, OpsPortalMixin, View):
    def post(self, request, pk):
        JobOpening.objects.filter(pk=pk).delete()
        return HttpResponse('')


class DgcApplicationsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/dgc_applications.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        applications = DgcApplication.objects.select_related('partner_user')
        ctx['page_title'] = 'DGC Applications'
        ctx['status_choices'] = DgcApplication.STATUS_CHOICES
        ctx['status_counts'] = status_counts_for(applications, DgcApplication.STATUS_CHOICES)
        ctx['total_count'] = applications.count()
        page = paginate(self.request, applications)
        ctx['applications'] = page.object_list
        ctx['paginator_page'] = page
        return ctx


class DgcApplicationApproveView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        try:
            user, temp_password = approve_dgc_application(application, request.user)
            if temp_password:
                messages.success(
                    request,
                    f'Approved {application.name}. Share login → Username: {user.username} | Temp password: {temp_password} → /auth/login/ then /dashboard/dgc/',
                )
            else:
                messages.success(
                    request,
                    f'Approved {application.name}. Google account unlocked — they can use /dashboard/dgc/ now.',
                )
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('operations:dgc_applications')


class DgcApplicationRejectView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        if application.status in (
            DgcApplication.STATUS_APPROVED,
            DgcApplication.STATUS_PAUSED,
            DgcApplication.STATUS_CANCELLED,
        ):
            messages.error(request, 'Use Pause or Cancel for approved partners — cannot reject.')
        else:
            application.status = DgcApplication.STATUS_REJECTED
            application.reviewed_by = request.user
            application.save(update_fields=['status', 'reviewed_by', 'updated_at'])
            messages.success(request, f'Rejected {application.name}.')
        return redirect('operations:dgc_applications')


class DgcApplicationPauseView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        try:
            pause_dgc_application(application, request.user)
            messages.success(request, f'Paused {application.name} — portal login disabled.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('operations:dgc_applications')


class DgcApplicationResumeView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        try:
            resume_dgc_application(application, request.user)
            messages.success(request, f'Resumed {application.name} — portal login enabled.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('operations:dgc_applications')


class DgcApplicationCancelView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        from django.contrib import messages

        application = get_object_or_404(DgcApplication, pk=pk)
        try:
            cancel_dgc_application(application, request.user)
            messages.success(request, f'Cancelled {application.name} — portal permanently disabled.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('operations:dgc_applications')


class DgcLeadsView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/dgc_leads.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        leads = PartnerLead.objects.select_related(
            'partner', 'partner__user',
        ).all()
        ctx['page_title'] = 'DGC Leads'
        ctx['status_choices'] = PartnerLead.STATUS_CHOICES
        ctx['status_counts'] = status_counts_for(leads, PartnerLead.STATUS_CHOICES)
        ctx['total_count'] = leads.count()
        page = paginate(self.request, leads)
        ctx['leads'] = page.object_list
        ctx['paginator_page'] = page
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
            update_partner_lead_status(lead, status)
            lead.refresh_from_db()
        return render(request, 'partials/ops/_dgc_lead_row.jinja', {
            'lead': lead,
            'status_choices': PartnerLead.STATUS_CHOICES,
        })


class DgcOrdersView(SuperAdminRequiredMixin, OpsBaseMixin, TemplateView):
    template_name = 'pages/ops/dgc_orders.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orders = PartnerOrder.objects.select_related(
            'partner', 'partner__user', 'offer', 'assigned_to',
        ).all()
        ctx['page_title'] = 'DGC Orders'
        ctx['status_choices'] = PartnerOrder.STATUS_CHOICES
        ctx['status_counts'] = status_counts_for(orders, PartnerOrder.STATUS_CHOICES)
        ctx['total_count'] = orders.count()
        page = paginate(self.request, orders)
        ctx['orders'] = page.object_list
        ctx['paginator_page'] = page
        ctx['delivery_users'] = _delivery_users()
        return ctx


class DgcOrderStatusUpdateView(OpsPortalMixin, View):
    """Admin or assigned delivery user can update order status."""

    def post(self, request, pk):
        order = get_object_or_404(
            PartnerOrder.objects.select_related('partner', 'partner__user', 'offer', 'assigned_to'),
            pk=pk,
        )
        is_superuser = _is_superuser(request.user)
        is_assignee = order.assigned_to_id == request.user.id
        if not (is_superuser or is_assignee):
            return redirect(get_dashboard_url_for_user(request.user))
        status = request.POST.get('status')
        valid = {value for value, _ in PartnerOrder.STATUS_CHOICES}
        if not is_superuser:
            # Cancelling voids the partner's commission — a delivery-desk
            # assignee can move work forward but can't unilaterally kill
            # someone else's earnings; that stays with ops management.
            valid = valid - {PartnerOrder.STATUS_CANCELLED}
        if status in valid:
            update_order_status(order, status)
            order.refresh_from_db()
        if request.headers.get('HX-Request'):
            return render(request, 'partials/ops/_dgc_order_row.jinja', _dgc_order_row_context(order))
        return redirect('operations:my_work')


def _delivery_users():
    from django.contrib.auth.models import User
    return User.objects.filter(
        profile__role__in=DELIVERY_ROLES,
        is_active=True,
    ).select_related('profile').order_by('first_name', 'username')


def _dgc_order_row_context(order):
    return {
        'order': order,
        'status_choices': PartnerOrder.STATUS_CHOICES,
        'delivery_users': _delivery_users(),
    }


class DgcOrderAssignView(SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(
            PartnerOrder.objects.select_related('partner', 'partner__user', 'offer', 'assigned_to'),
            pk=pk,
        )
        form = OrderAssignForm(request.POST)
        if form.is_valid():
            assign_order(
                order,
                form.cleaned_data.get('assigned_to'),
                due_at=form.cleaned_data.get('due_at'),
                work_notes=form.cleaned_data.get('work_notes') or '',
            )
            order.refresh_from_db()
        return render(request, 'partials/ops/_dgc_order_row.jinja', _dgc_order_row_context(order))


class MyWorkView(OpsBaseMixin, TemplateView):
    """Delivery desk — orders assigned to the logged-in freelancer/dev."""

    template_name = 'pages/ops/my_work.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'My Work'
        orders = PartnerOrder.objects.filter(
            assigned_to=self.request.user,
        ).exclude(
            status=PartnerOrder.STATUS_CANCELLED,
        ).select_related('partner', 'partner__user', 'offer')
        ctx['orders'] = orders
        ctx['status_choices'] = [
            c for c in PartnerOrder.STATUS_CHOICES if c[0] != PartnerOrder.STATUS_CANCELLED
        ]
        return ctx


class OpsDashboardV2View(OpsBaseMixin, TemplateView):
    """Redesigned Mission Control at /ops2/."""

    template_name = 'pages/ops/mission_v2.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mission Control'
        include_jobs = ctx.get('is_superuser_ops', False)
        ctx.update(get_mission_control_context(include_jobs=include_jobs))
        return ctx


class OpsMissionLiveV2View(OpsPortalMixin, View):
    def get(self, request):
        include_jobs = _is_superuser(request.user)
        ctx = get_mission_control_context(include_jobs=include_jobs)
        ctx['is_superuser_ops'] = include_jobs
        return render(request, 'partials/ops/_mission_live_v2.jinja', ctx)
