from decimal import Decimal

from django.db import models

from clients.models import ClientAccount
from projects.models import Project


class Invoice(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT, 'Sent'),
        (STATUS_PAID, 'Paid'),
        (STATUS_OVERDUE, 'Overdue'),
    ]

    client_account = models.ForeignKey(
        ClientAccount, on_delete=models.CASCADE, related_name='invoices',
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices',
    )
    invoice_number = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SENT)
    due_date = models.DateField()
    issued_at = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at', '-created_at']

    def __str__(self):
        return f'{self.invoice_number} — {self.client_account.company_name}'
