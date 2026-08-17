"""Shared Razorpay client helpers — used by billing (invoices) and academy
(course-fee checkout) so neither app needs to know about the other."""
from decimal import Decimal

import razorpay
from django.conf import settings


def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_order(amount, receipt, notes=None):
    """Amount is rupees (Decimal/str/int); Razorpay's API wants paise."""
    client = get_razorpay_client()
    amount_paise = int(Decimal(amount) * 100)
    return client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': receipt,
        'notes': notes or {},
    })


def verify_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Raises razorpay.errors.SignatureVerificationError on failure."""
    client = get_razorpay_client()
    client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature,
    })


def fetch_payment(razorpay_payment_id):
    """Razorpay's own record of the payment — includes the email/contact the
    buyer entered into the Checkout widget when we don't collect it ourselves."""
    client = get_razorpay_client()
    return client.payment.fetch(razorpay_payment_id)
