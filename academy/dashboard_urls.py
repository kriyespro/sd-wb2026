from django.urls import path

from . import dashboard_views as views

app_name = 'academy_dashboard'

urlpatterns = [
    path('', views.StudentDashboardView.as_view(), name='dashboard'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('assignments/', views.AssignmentsView.as_view(), name='assignments'),
    path('assignments/<int:pk>/submit/', views.AssignmentSubmitView.as_view(), name='assignment_submit'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('mentor/', views.MentorView.as_view(), name='mentor'),
    path('attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('portfolio/add/', views.PortfolioAddView.as_view(), name='portfolio_add'),
    path('certificates/', views.CertificatesView.as_view(), name='certificates'),
    path('interview-prep/', views.InterviewPrepView.as_view(), name='interview_prep'),
    path('placement/', views.PlacementView.as_view(), name='placement'),
]
