from django.conf import settings
from django.db import models


class Lead(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_QUALIFIED = 'qualified'
    STATUS_PROPOSAL = 'proposal'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_QUALIFIED, 'Qualified'),
        (STATUS_PROPOSAL, 'Proposal'),
        (STATUS_WON, 'Won'),
        (STATUS_LOST, 'Lost'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    service_interest = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    source_page = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads',
    )
    handoff_notes = models.TextField(blank=True)
    converted_client = models.ForeignKey(
        'clients.ClientAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_leads',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.email}'

    @property
    def is_converted(self):
        return self.converted_client_id is not None
