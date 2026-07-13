from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.crypto import get_random_string

from users.roles import ROLE_PARTNER

from .models import (
    Commission,
    DgcApplication,
    PartnerLead,
    PartnerOrder,
    PartnerProfile,
    PayoutRequest,
    ResellerOffer,
)

DGC_NAV = [
    {'title': 'Offers', 'icon': '📦', 'url_name': 'partners:offers'},
    {'title': 'Orders', 'icon': '🛒', 'url_name': 'partners:orders'},
    {'title': 'Leads', 'icon': '📞', 'url_name': 'partners:leads'},
    {'title': 'Commissions', 'icon': '💰', 'url_name': 'partners:commissions'},
    {'title': 'Payouts', 'icon': '🏦', 'url_name': 'partners:payouts'},
]


def get_partner_profile(user):
    return getattr(user, 'partner_profile', None)


def create_dgc_application(form):
    return form.save()


def _unique_partner_code(name):
    base = ''.join(ch for ch in name.upper() if ch.isalnum())[:4] or 'DGC'
    for _ in range(20):
        code = f'{base}{get_random_string(4, allowed_chars="0123456789")}'
        if not PartnerProfile.objects.filter(code=code).exists():
            return code
    return f'DGC{get_random_string(6, allowed_chars="0123456789")}'


@transaction.atomic
def approve_dgc_application(application, actor):
    """Approve application and create partner login. Returns (user, temp_password)."""
    if application.status == DgcApplication.STATUS_APPROVED and application.partner_user_id:
        raise ValueError('Application already approved')

    email = application.email.strip().lower()
    username_base = email.split('@')[0][:20]
    username = username_base
    n = 1
    while User.objects.filter(username=username).exists():
        username = f'{username_base}{n}'
        n += 1

    temp_password = get_random_string(10)
    user = User.objects.create_user(
        username=username,
        email=email,
        password=temp_password,
        first_name=application.name.split()[0][:30],
        last_name=' '.join(application.name.split()[1:])[:30],
    )
    user.profile.role = ROLE_PARTNER
    user.profile.phone = application.phone
    user.profile.save(update_fields=['role', 'phone'])

    PartnerProfile.objects.create(
        user=user,
        code=_unique_partner_code(application.name),
    )

    application.status = DgcApplication.STATUS_APPROVED
    application.reviewed_by = actor
    application.partner_user = user
    application.temp_password = temp_password
    application.save(update_fields=[
        'status', 'reviewed_by', 'partner_user', 'temp_password', 'updated_at',
    ])
    return user, temp_password


def _set_partner_access(application, *, active: bool):
    user = application.partner_user
    if not user:
        raise ValueError('No partner login linked to this application')
    if user.is_active != active:
        user.is_active = active
        user.save(update_fields=['is_active'])
    partner = getattr(user, 'partner_profile', None)
    if partner and partner.is_active != active:
        partner.is_active = active
        partner.save(update_fields=['is_active'])


@transaction.atomic
def pause_dgc_application(application, actor):
    """Temporarily disable portal access; can resume later."""
    if application.status != DgcApplication.STATUS_APPROVED:
        raise ValueError('Only approved applications can be paused')
    _set_partner_access(application, active=False)
    application.status = DgcApplication.STATUS_PAUSED
    application.reviewed_by = actor
    application.save(update_fields=['status', 'reviewed_by', 'updated_at'])


@transaction.atomic
def resume_dgc_application(application, actor):
    """Re-enable a paused partner portal."""
    if application.status != DgcApplication.STATUS_PAUSED:
        raise ValueError('Only paused applications can be resumed')
    _set_partner_access(application, active=True)
    application.status = DgcApplication.STATUS_APPROVED
    application.reviewed_by = actor
    application.save(update_fields=['status', 'reviewed_by', 'updated_at'])


@transaction.atomic
def cancel_dgc_application(application, actor):
    """Permanently cancel after approve — disables login; no resume."""
    if application.status not in (
        DgcApplication.STATUS_APPROVED,
        DgcApplication.STATUS_PAUSED,
    ):
        raise ValueError('Only approved or paused applications can be cancelled')
    _set_partner_access(application, active=False)
    application.status = DgcApplication.STATUS_CANCELLED
    application.reviewed_by = actor
    application.save(update_fields=['status', 'reviewed_by', 'updated_at'])


def get_active_offers():
    return ResellerOffer.objects.filter(is_active=True)


@transaction.atomic
def place_order(partner, offer, quantity=1, notes=''):
    quantity = max(1, int(quantity))
    total = offer.price * quantity
    order = PartnerOrder.objects.create(
        partner=partner,
        offer=offer,
        quantity=quantity,
        unit_price=offer.price,
        total=total,
        notes=notes or '',
        status=PartnerOrder.STATUS_PENDING,
    )
    commission_amount = (total * offer.commission_percent / Decimal('100')).quantize(Decimal('0.01'))
    if commission_amount > 0:
        Commission.objects.create(
            partner=partner,
            amount=commission_amount,
            source=Commission.SOURCE_ORDER,
            order=order,
            note=f'{offer.commission_percent}% of order #{order.pk}',
        )
    return order


def create_partner_lead(partner, cleaned):
    return PartnerLead.objects.create(partner=partner, **cleaned)


@transaction.atomic
def update_lead_status(lead, status):
    prev = lead.status
    lead.status = status
    lead.save(update_fields=['status', 'updated_at'])
    if status == PartnerLead.STATUS_WON and prev != PartnerLead.STATUS_WON:
        if not lead.commissions.exists() and lead.deal_value > 0:
            # Use average active offer % or default 20%
            offer = get_active_offers().first()
            pct = offer.commission_percent if offer else Decimal('20.00')
            amount = (lead.deal_value * pct / Decimal('100')).quantize(Decimal('0.01'))
            Commission.objects.create(
                partner=lead.partner,
                amount=amount,
                source=Commission.SOURCE_LEAD,
                lead=lead,
                note=f'{pct}% of won lead deal value',
            )
    return lead


def partner_commission_summary(partner):
    qs = Commission.objects.filter(partner=partner)
    def total(status):
        return qs.filter(status=status).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')

    return {
        'pending': total(Commission.STATUS_PENDING),
        'requested': total(Commission.STATUS_REQUESTED),
        'paid': total(Commission.STATUS_PAID),
        'available': total(Commission.STATUS_PENDING),
    }


def can_request_payout(today=None):
    today = today or timezone.localdate()
    return today.day == 21


def create_payout_request(partner, today=None):
    today = today or timezone.localdate()
    if not can_request_payout(today):
        raise ValueError('Payout requests are only accepted on the 21st of each month')

    pending = list(
        Commission.objects.filter(partner=partner, status=Commission.STATUS_PENDING),
    )
    if not pending:
        raise ValueError('No pending commission available for payout')

    month_start = PayoutRequest.month_start(today)
    if PayoutRequest.objects.filter(partner=partner, period_month=month_start).exists():
        raise ValueError('Payout already requested for this month')

    amount = sum((c.amount for c in pending), Decimal('0.00'))
    with transaction.atomic():
        payout = PayoutRequest.objects.create(
            partner=partner,
            amount=amount,
            period_month=month_start,
            status=PayoutRequest.STATUS_PENDING,
        )
        Commission.objects.filter(
            pk__in=[c.pk for c in pending],
        ).update(status=Commission.STATUS_REQUESTED)
    return payout


def get_partner_dashboard_stats(partner):
    leads = partner.leads.all()
    summary = partner_commission_summary(partner)
    today = timezone.localdate()
    return {
        'open_leads': leads.exclude(status__in=[PartnerLead.STATUS_WON, PartnerLead.STATUS_LOST]).count(),
        'won_leads': leads.filter(status=PartnerLead.STATUS_WON).count(),
        'orders': partner.orders.count(),
        'pending_commission': summary['pending'],
        'requested_commission': summary['requested'],
        'paid_commission': summary['paid'],
        'can_payout': can_request_payout(today),
        'payout_day': 21,
        'today': today,
    }
