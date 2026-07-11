from django.urls import path

from . import views

app_name = 'operations'

urlpatterns = [
    path('', views.OpsDashboardView.as_view(), name='dashboard'),
    path('live/mission/', views.OpsMissionLiveView.as_view(), name='live_mission'),
    path('live/leads/', views.OpsLeadsLiveView.as_view(), name='live_leads'),
    path('quality-check/', views.QualityCheckView.as_view(), name='quality_check'),
    path('quality-check/<int:pk>/approve/', views.DeliverableApproveView.as_view(), name='deliverable_approve'),
    path('quality-check/<int:pk>/reject/', views.DeliverableRejectView.as_view(), name='deliverable_reject'),
    path('projects/', views.OpsProjectsView.as_view(), name='projects'),
    path('pipeline/', views.PipelineView.as_view(), name='pipeline'),
    path('allocation/', views.AllocationView.as_view(), name='allocation'),
    path('allocation/add/', views.AllocationCreateView.as_view(), name='allocation_add'),
    path('mentors/', views.MentorsView.as_view(), name='mentors'),
    path('mentors/allocate/', views.MentorAllocateView.as_view(), name='mentor_allocate'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('performance/', views.PerformanceView.as_view(), name='performance'),
    path('leads/', views.LeadsView.as_view(), name='leads'),
    path('leads/<int:pk>/status/', views.LeadStatusUpdateView.as_view(), name='lead_status'),
    path('leads/<int:pk>/assign/', views.LeadAssignView.as_view(), name='lead_assign'),
    path('leads/<int:pk>/notes/', views.LeadNotesUpdateView.as_view(), name='lead_notes'),
    path('leads/<int:pk>/convert/', views.LeadConvertView.as_view(), name='lead_convert'),
    path('invoices/', views.OpsInvoicesView.as_view(), name='invoices'),
    path('job-applications/', views.JobApplicationsView.as_view(), name='job_applications'),
    path(
        'job-applications/<int:pk>/status/',
        views.JobApplicationStatusUpdateView.as_view(),
        name='job_application_status',
    ),
    path('dgc-applications/', views.DgcApplicationsView.as_view(), name='dgc_applications'),
    path(
        'dgc-applications/<int:pk>/approve/',
        views.DgcApplicationApproveView.as_view(),
        name='dgc_application_approve',
    ),
    path(
        'dgc-applications/<int:pk>/reject/',
        views.DgcApplicationRejectView.as_view(),
        name='dgc_application_reject',
    ),
    path('dgc-leads/', views.DgcLeadsView.as_view(), name='dgc_leads'),
    path(
        'dgc-leads/<int:pk>/status/',
        views.DgcLeadStatusUpdateView.as_view(),
        name='dgc_lead_status',
    ),
]
