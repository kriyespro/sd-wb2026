from decimal import Decimal

import razorpay
from django.conf import settings
from django.utils import timezone

from clients.models import ClientAccount

from .models import Invoice


def get_client_invoices(account):
    if not account:
        return Invoice.objects.none()
    return Invoice.objects.filter(client_account=account).select_related('project')


def get_all_invoices():
    return Invoice.objects.select_related('client_account', 'project')


def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(invoice):
    """Create (or reuse) a Razorpay order for this invoice and store its id.

    Amount is paise (Razorpay's base unit); Invoice.amount is stored in rupees.
    """
    if invoice.status == Invoice.STATUS_PAID:
        raise ValueError('Invoice is already paid')

    client = get_razorpay_client()
    amount_paise = int(Decimal(invoice.amount) * 100)
    order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': invoice.invoice_number,
        'notes': {'invoice_id': str(invoice.pk)},
    })
    invoice.razorpay_order_id = order['id']
    invoice.save(update_fields=['razorpay_order_id'])
    return order


def verify_and_mark_paid(invoice, razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify the payment signature server-side before trusting the client's
    callback — the client's `handler` payload is not itself proof of payment."""
    if invoice.status == Invoice.STATUS_PAID:
        return invoice
    if invoice.razorpay_order_id != razorpay_order_id:
        raise ValueError('Order mismatch')

    client = get_razorpay_client()
    client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature,
    })

    invoice.status = Invoice.STATUS_PAID
    invoice.razorpay_payment_id = razorpay_payment_id
    invoice.paid_at = timezone.now()
    invoice.save(update_fields=['status', 'razorpay_payment_id', 'paid_at'])
    return invoice
