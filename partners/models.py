from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class DgcApplication(models.Model):
    STATUS_NEW = 'new'
    STATUS_REVIEW = 'review'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEW, 'Under Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=120, blank=True)
    experience = models.CharField(max_length=200, blank=True)
    why = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_dgc_applications',
    )
    partner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_dgc_application',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.email}'


class PartnerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner_profile',
    )
    code = models.CharField(max_length=20, unique=True)
    upi_id = models.CharField(max_length=120, blank=True)
    bank_account = models.CharField(max_length=120, blank=True)
    bank_ifsc = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'DGC {self.code} — {self.user.username}'


class ResellerOffer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    commission_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('20.00'),
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title


class PartnerOrder(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_FULFILLED, 'Fulfilled'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name='orders',
    )
    offer = models.ForeignKey(
        ResellerOffer, on_delete=models.PROTECT, related_name='orders',
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.offer.title}'


class PartnerLead(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_WON, 'Won'),
        (STATUS_LOST, 'Lost'),
    ]

    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name='leads',
    )
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=120, blank=True)
    interest = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    deal_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.get_status_display()}'


class Commission(models.Model):
    SOURCE_ORDER = 'order'
    SOURCE_LEAD = 'lead'
    SOURCE_CHOICES = [
        (SOURCE_ORDER, 'Order'),
        (SOURCE_LEAD, 'Lead'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_REQUESTED = 'requested'
    STATUS_PAID = 'paid'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REQUESTED, 'Requested'),
        (STATUS_PAID, 'Paid'),
    ]

    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name='commissions',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    order = models.ForeignKey(
        PartnerOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions',
    )
    lead = models.ForeignKey(
        PartnerLead, on_delete=models.SET_NULL, null=True, blank=True, related_name='commissions',
    )
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} — {self.partner.code} ({self.status})'


class PayoutRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_PAID = 'paid'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_PAID, 'Paid'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    partner = models.ForeignKey(
        PartnerProfile, on_delete=models.CASCADE, related_name='payout_requests',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period_month = models.DateField(help_text='First day of the payout month')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [('partner', 'period_month')]

    def __str__(self):
        return f'Payout {self.period_month:%b %Y} — {self.partner.code}'

    @staticmethod
    def month_start(dt=None):
        dt = dt or timezone.localdate()
        return dt.replace(day=1)
