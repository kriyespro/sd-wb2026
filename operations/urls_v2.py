from django.urls import path

from . import views

app_name = 'ops2'

urlpatterns = [
    path('', views.OpsDashboardV2View.as_view(), name='dashboard'),
    path('live/', views.OpsMissionLiveV2View.as_view(), name='live'),
]
