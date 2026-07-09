from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientDashboardView.as_view(), name='dashboard'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('files/', views.FilesView.as_view(), name='files'),
    path('meetings/', views.MeetingsView.as_view(), name='meetings'),
    path('invoices/', views.InvoicesView.as_view(), name='invoices'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('support/new/', views.SupportTicketCreateView.as_view(), name='ticket_create'),
    path('support/<int:pk>/', views.SupportTicketDetailView.as_view(), name='ticket_detail'),
    path('support/<int:pk>/reply/', views.SupportTicketReplyView.as_view(), name='ticket_reply'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('goals/', views.GoalsView.as_view(), name='goals'),
    path('roi/', views.ROIView.as_view(), name='roi'),
]
