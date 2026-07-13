from django.urls import path

from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.KnowledgeIndexView.as_view(), name='index'),
    path('<slug:slug>/', views.KnowledgeDetailView.as_view(), name='detail'),
]
