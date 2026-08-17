from django.utils import timezone

from clients.models import ClientAccount
from core.razorpay_utils import create_order, get_razorpay_client, verify_signature

from .models import Invoice

__all__ = [
    'get_client_invoices', 'get_all_invoices', 'get_razorpay_client',
    'create_razorpay_order', 'verify_and_mark_paid',
]


def get_client_invoices(account):
    if not account:
        return Invoice.objects.none()
    return Invoice.objects.filter(client_account=account).select_related('project')


def get_all_invoices():
    return Invoice.objects.select_related('client_account', 'project')


def create_razorpay_order(invoice):
    """Create (or reuse) a Razorpay order for this invoice and store its id."""
    if invoice.status == Invoice.STATUS_PAID:
        raise ValueError('Invoice is already paid')

    order = create_order(invoice.amount, invoice.invoice_number, {'invoice_id': str(invoice.pk)})
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

    verify_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)

    invoice.status = Invoice.STATUS_PAID
    invoice.razorpay_payment_id = razorpay_payment_id
    invoice.paid_at = timezone.now()
    invoice.save(update_fields=['status', 'razorpay_payment_id', 'paid_at'])
    return invoice
