from django.urls import path

from . import public_views

app_name = 'partners_public'

urlpatterns = [
    path('', public_views.DgcLandingView.as_view(), name='landing'),
    path('apply/', public_views.DgcApplyView.as_view(), name='apply'),
]
