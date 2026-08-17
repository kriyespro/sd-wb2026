from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from core.pagination import paginate
from users.mixins import DashboardContextMixin, StudentPortalMixin
from users.services import get_dashboard_url_for_user

from . import fourd_services
from .forms import (
    ActivityLogForm,
    DailyFourDForm,
    PortfolioItemForm,
    StudentLeadForm,
    StudentLeadStatusForm,
    StudentProjectUpdateForm,
    SubmissionForm,
    TeachingSessionForm,
)
from .models import Assignment, Course, Enrollment, StudentLead, StudentTask, Submission
from .services import (
    STUDENT_NAV,
    add_portfolio_item,
    create_student_lead,
    create_teaching_session,
    get_enrolled_courses,
    get_mentor_for_student,
    get_student_assignments,
    get_student_attention_items,
    get_student_stats,
    log_activity,
    mark_task_done,
    save_daily_notes,
    submit_assignment,
    update_student_lead_status,
)


class StudentBaseMixin(DashboardContextMixin, StudentPortalMixin):
    portal_name = 'Academy Portal'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['sidebar_links'] = STUDENT_NAV
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        return ctx


class StudentDashboardView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Student Dashboard'
        ctx['stats'] = get_student_stats(self.request.user)
        ctx['attention_items'] = get_student_attention_items(self.request.user)
        ctx['recent_tasks'] = self.request.user.student_tasks.all()[:5]
        ctx['mentor'] = get_mentor_for_student(self.request.user)
        ctx['pillar_status'] = fourd_services.pillar_status(self.request.user, timezone.localdate())
        ctx['daily_score'] = fourd_services.daily_score(self.request.user)
        return ctx


class CoursesView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/courses.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Courses'
        ctx['enrollments'] = Enrollment.objects.filter(
            user=self.request.user,
        ).select_related('course')
        return ctx


class CourseDetailView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/course_detail.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = get_object_or_404(
            get_enrolled_courses(self.request.user), slug=kwargs['slug'],
        )
        ctx['page_title'] = course.title
        ctx['course'] = course
        ctx['enrollment'] = Enrollment.objects.get(user=self.request.user, course=course)
        return ctx


class AssignmentsView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/assignments.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Assignments'
        assignments = get_student_assignments(self.request.user)
        submissions = {
            s.assignment_id: s for s in Submission.objects.filter(user=self.request.user)
        }
        ctx['assignments'] = assignments
        ctx['submitted_ids'] = set(submissions)
        ctx['submissions'] = submissions
        return ctx


class AssignmentSubmitView(StudentPortalMixin, View):
    def post(self, request, pk):
        course_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
        assignment = get_object_or_404(Assignment, pk=pk, course_id__in=course_ids)
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submit_assignment(request.user, assignment, form.cleaned_data['content'])
            return render(request, 'partials/_submission_success.jinja', {
                'assignment': assignment,
            })
        return render(request, 'partials/_submission_form.jinja', {
            'assignment': assignment,
            'form': form,
            'show_errors': True,
        })


class TasksView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/tasks.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Tasks'
        ctx['tasks'] = self.request.user.student_tasks.all()
        return ctx


class TaskCompleteView(StudentPortalMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(StudentTask, pk=pk, user=request.user)
        if task.status != StudentTask.STATUS_DONE:
            mark_task_done(task)
        return redirect('academy_dashboard:tasks')


class ProjectsView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/projects.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Projects'
        ctx['projects'] = self.request.user.student_projects.all()
        ctx['form'] = StudentProjectUpdateForm()
        return ctx


class ProjectUpdateView(StudentPortalMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(request.user.student_projects, pk=pk)
        form = StudentProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
        return redirect('academy_dashboard:projects')


class MentorView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/mentor.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mentor'
        ctx['mentor'] = get_mentor_for_student(self.request.user)
        allocation = getattr(self.request.user, 'mentor_allocation', None)
        ctx['allocation'] = allocation
        return ctx


class AttendanceView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/attendance.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Attendance'
        all_records = self.request.user.attendance_records.all()
        counts = all_records.aggregate(
            total=Count('id'), present=Count('id', filter=Q(status='present')),
        )
        page = paginate(self.request, all_records)
        ctx['records'] = page.object_list
        ctx['paginator_page'] = page
        ctx['attendance_rate'] = (
            round((counts['present'] / counts['total']) * 100) if counts['total'] else 0
        )
        return ctx


class PortfolioView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/portfolio.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Portfolio'
        ctx['items'] = self.request.user.portfolio_items.all()
        ctx['form'] = PortfolioItemForm()
        return ctx


class PortfolioAddView(StudentPortalMixin, View):
    def post(self, request):
        form = PortfolioItemForm(request.POST)
        if form.is_valid():
            add_portfolio_item(request.user, form)
            return redirect('academy_dashboard:portfolio')
        return render(request, 'pages/dashboard/student/portfolio.jinja', {
            'page_title': 'Portfolio',
            'portal_name': 'Academy Portal',
            'sidebar_links': STUDENT_NAV,
            'dashboard_url': get_dashboard_url_for_user(request.user),
            'items': request.user.portfolio_items.all(),
            'form': form,
            'show_errors': True,
        })


class CertificatesView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/certificates.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Certificates'
        ctx['certificates'] = self.request.user.certificates.select_related('course')
        return ctx


class InterviewPrepView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/interview_prep.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Interview Prep'
        ctx['resources'] = [
            {'title': 'Common Interview Questions', 'desc': 'Top 50 digital marketing interview Q&A'},
            {'title': 'Portfolio Review Checklist', 'desc': 'What recruiters look for in your portfolio'},
            {'title': 'Salary Negotiation Guide', 'desc': 'How to negotiate your first offer'},
            {'title': 'LinkedIn Optimization', 'desc': 'Build a recruiter-friendly profile'},
        ]
        return ctx


class PlacementView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/placement.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Placement'
        ctx['applications'] = self.request.user.placement_applications.all()
        return ctx


class FourDPlannerView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/fourd.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()
        ctx['page_title'] = 'Daily 4D'
        ctx['pillar_status'] = fourd_services.pillar_status(user, today)
        ctx['pillar_weights'] = fourd_services.PILLAR_WEIGHTS
        ctx['daily_score'] = fourd_services.daily_score(user, today)
        ctx['score_level'] = fourd_services.score_level(ctx['daily_score'])
        ctx['rolling_average'] = fourd_services.rolling_average(user)
        ctx['today_tasks'] = user.student_tasks.exclude(status=StudentTask.STATUS_DONE).exclude(
            stage=StudentTask.STAGE_GENERAL,
        )
        ctx['today_log'] = user.daily_fourd_logs.filter(date=today).first()
        ctx['form'] = DailyFourDForm(initial={'notes': ctx['today_log'].notes if ctx['today_log'] else ''})
        ctx['activity_form'] = ActivityLogForm()
        ctx['recent_activity'] = fourd_services.get_activity_feed(user, limit=5)
        return ctx


class FourDSubmitView(StudentPortalMixin, View):
    def post(self, request):
        form = DailyFourDForm(request.POST)
        if form.is_valid():
            save_daily_notes(request.user, timezone.localdate(), form.cleaned_data['notes'])
            messages.success(request, "Today's 4D log saved.")
        return redirect('academy_dashboard:fourd')


class ActivityLogCreateView(StudentPortalMixin, View):
    def post(self, request):
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            log_activity(request.user, form.cleaned_data)
            messages.success(request, 'Activity logged.')
        redirect_to = 'academy_dashboard:progress' if request.POST.get('next') == 'progress' else 'academy_dashboard:fourd'
        return redirect(redirect_to)


class ProgressView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/progress.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['page_title'] = 'My Progress'
        ctx['daily_score'] = fourd_services.daily_score(user)
        ctx['score_level'] = fourd_services.score_level(ctx['daily_score'])
        ctx['score_history'] = fourd_services.get_score_history(user)
        ctx['activity_feed'] = fourd_services.get_activity_feed(user)
        ctx['pillar_totals'] = fourd_services.get_pillar_totals(user)
        ctx['streak'] = fourd_services.current_streak(user)
        ctx['activity_form'] = ActivityLogForm()
        return ctx


class TeachingListView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/teaching.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Teaching'
        ctx['sessions'] = self.request.user.teaching_sessions.all()
        ctx['form'] = TeachingSessionForm()
        return ctx


class TeachingCreateView(StudentPortalMixin, View):
    def post(self, request):
        form = TeachingSessionForm(request.POST)
        if form.is_valid():
            create_teaching_session(request.user, form.cleaned_data)
        return redirect('academy_dashboard:teaching')


class FieldLeadsView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/field.jinja'
    feature_tag = '4D'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Field CRM'
        ctx['leads'] = self.request.user.field_leads.all()
        ctx['form'] = StudentLeadForm()
        ctx['status_form'] = StudentLeadStatusForm()
        return ctx


class FieldLeadCreateView(StudentPortalMixin, View):
    def post(self, request):
        form = StudentLeadForm(request.POST)
        if form.is_valid():
            create_student_lead(request.user, form.cleaned_data)
        return redirect('academy_dashboard:field_leads')


class FieldLeadStatusView(StudentPortalMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(StudentLead, pk=pk, user=request.user)
        form = StudentLeadStatusForm(request.POST)
        if form.is_valid():
            update_student_lead_status(lead, form.cleaned_data['status'])
        return redirect('academy_dashboard:field_leads')
