from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('our-work/', views.our_work, name='our_work'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
    path('industries/', views.industries, name='industries'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('startup/', views.startup, name='startup'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    path('lead/submit/', views.lead_submit, name='lead_submit'),
]
