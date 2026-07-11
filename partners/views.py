from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from users.mixins import DashboardContextMixin, PartnerPortalMixin
from users.services import get_dashboard_url_for_user

from .forms import (
    PartnerLeadForm,
    PartnerOrderForm,
    PartnerPayoutDetailsForm,
)
from .services import (
    DGC_NAV,
    can_request_payout,
    create_partner_lead,
    create_payout_request,
    get_active_offers,
    get_partner_dashboard_stats,
    get_partner_profile,
    partner_commission_summary,
    place_order,
)


class PartnerBaseMixin(DashboardContextMixin, PartnerPortalMixin):
    portal_name = 'DGC Portal'
    dashboard_label = 'DGC Home'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portal_name'] = self.portal_name
        ctx['dashboard_label'] = self.dashboard_label
        ctx['sidebar_links'] = DGC_NAV
        ctx['dashboard_url'] = get_dashboard_url_for_user(self.request.user)
        ctx['partner'] = get_partner_profile(self.request.user)
        return ctx


class PartnerDashboardView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/index.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'DGC Dashboard'
        partner = ctx['partner']
        if partner:
            ctx['stats'] = get_partner_dashboard_stats(partner)
            ctx['recent_leads'] = partner.leads.all()[:5]
            ctx['recent_orders'] = partner.orders.select_related('offer')[:5]
            ctx['recent_commissions'] = partner.commissions.all()[:5]
            ctx['lead_form'] = PartnerLeadForm()
        else:
            ctx['stats'] = {}
            ctx['lead_form'] = None
        return ctx


class OffersView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/offers.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Reseller Offers'
        ctx['offers'] = get_active_offers()
        return ctx


class OrdersView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/orders.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Orders'
        partner = ctx['partner']
        offers = get_active_offers()
        ctx['form'] = PartnerOrderForm(offers=offers)
        ctx['orders'] = partner.orders.select_related('offer') if partner else []
        return ctx


class OrderCreateView(PartnerBaseMixin, View):
    def post(self, request):
        partner = get_partner_profile(request.user)
        if not partner or not partner.is_active:
            messages.error(request, 'Partner profile inactive.')
            return redirect('partners:orders')
        form = PartnerOrderForm(request.POST, offers=get_active_offers())
        if form.is_valid():
            place_order(
                partner,
                form.cleaned_data['offer'],
                quantity=form.cleaned_data['quantity'],
                notes=form.cleaned_data.get('notes') or '',
            )
            messages.success(request, 'Order placed. Commission recorded as pending.')
        else:
            messages.error(request, 'Could not place order. Check the form.')
        return redirect('partners:orders')


class LeadsView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/leads.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Leads'
        partner = ctx['partner']
        ctx['form'] = PartnerLeadForm()
        ctx['leads'] = partner.leads.all() if partner else []
        return ctx


class LeadCreateView(PartnerBaseMixin, View):
    def post(self, request):
        partner = get_partner_profile(request.user)
        if not partner or not partner.is_active:
            messages.error(request, 'Partner profile inactive.')
            return redirect('partners:leads')
        form = PartnerLeadForm(request.POST)
        if form.is_valid():
            create_partner_lead(partner, form.cleaned_data)
            messages.success(request, 'Lead submitted.')
        else:
            messages.error(request, 'Could not submit lead. Check the form.')
        return redirect('partners:leads')


class CommissionsView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/commissions.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Commissions'
        partner = ctx['partner']
        ctx['summary'] = partner_commission_summary(partner) if partner else {}
        ctx['commissions'] = partner.commissions.select_related('order', 'lead') if partner else []
        return ctx


class PayoutsView(PartnerBaseMixin, TemplateView):
    template_name = 'pages/dashboard/dgc/payouts.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Payouts'
        partner = ctx['partner']
        ctx['can_payout'] = can_request_payout()
        ctx['summary'] = partner_commission_summary(partner) if partner else {}
        ctx['payouts'] = partner.payout_requests.all() if partner else []
        ctx['payout_form'] = PartnerPayoutDetailsForm(instance=partner) if partner else None
        return ctx


class PayoutRequestCreateView(PartnerBaseMixin, View):
    def post(self, request):
        partner = get_partner_profile(request.user)
        if not partner:
            return redirect('partners:payouts')
        try:
            create_payout_request(partner)
            messages.success(request, 'Payout request submitted for this month.')
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect('partners:payouts')


class PayoutDetailsUpdateView(PartnerBaseMixin, View):
    def post(self, request):
        partner = get_partner_profile(request.user)
        if not partner:
            return redirect('partners:payouts')
        form = PartnerPayoutDetailsForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payout details saved.')
        else:
            messages.error(request, 'Could not save payout details.')
        return redirect('partners:payouts')
