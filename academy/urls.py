from django.urls import path

from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:slug>/checkout/', views.checkout, name='checkout'),
    path('courses/<slug:slug>/enroll/', views.enroll_pay, name='enroll_pay'),
    path('courses/<slug:slug>/enroll/verify/<int:pk>/', views.enroll_verify, name='enroll_verify'),
    path('apply/', views.apply, name='apply'),
    path('apply/submit/', views.apply_submit, name='apply_submit'),
]
