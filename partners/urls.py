from django.urls import path

from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.PartnerDashboardView.as_view(), name='dashboard'),
    path('profile/', views.PartnerProfileView.as_view(), name='profile'),
    path('offers/', views.OffersView.as_view(), name='offers'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('orders/place/', views.OrderCreateView.as_view(), name='order_create'),
    path('leads/', views.LeadsView.as_view(), name='leads'),
    path('leads/new/', views.LeadCreateView.as_view(), name='lead_create'),
    path('commissions/', views.CommissionsView.as_view(), name='commissions'),
    path('payouts/', views.PayoutsView.as_view(), name='payouts'),
    path('payouts/request/', views.PayoutRequestCreateView.as_view(), name='payout_request'),
    path('payouts/details/', views.PayoutDetailsUpdateView.as_view(), name='payout_details'),
]
