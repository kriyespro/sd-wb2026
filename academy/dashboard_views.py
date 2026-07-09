from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from users.mixins import DashboardContextMixin, StudentPortalMixin
from users.services import get_dashboard_url_for_user

from .forms import PortfolioItemForm, SubmissionForm
from .models import Assignment, Course, Enrollment, Submission
from .services import (
    STUDENT_NAV,
    add_portfolio_item,
    get_enrolled_courses,
    get_mentor_for_student,
    get_student_assignments,
    get_student_stats,
    submit_assignment,
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
        ctx['recent_tasks'] = self.request.user.student_tasks.all()[:5]
        ctx['mentor'] = get_mentor_for_student(self.request.user)
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
        submitted_ids = set(
            Submission.objects.filter(user=self.request.user).values_list('assignment_id', flat=True),
        )
        ctx['assignments'] = assignments
        ctx['submitted_ids'] = submitted_ids
        ctx['submissions'] = {
            s.assignment_id: s for s in Submission.objects.filter(user=self.request.user)
        }
        return ctx


class AssignmentSubmitView(StudentPortalMixin, View):
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
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


class ProjectsView(StudentBaseMixin, TemplateView):
    template_name = 'pages/dashboard/student/projects.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Projects'
        ctx['projects'] = self.request.user.student_projects.all()
        return ctx


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
        records = self.request.user.attendance_records.all()
        ctx['records'] = records
        present = records.filter(status='present').count()
        total = records.count()
        ctx['attendance_rate'] = round((present / total) * 100) if total else 0
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
