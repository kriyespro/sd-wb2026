from django.conf import settings
from django.db import models


class ClientAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_account',
    )
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=120, blank=True)
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='managed_client_accounts',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class Goal(models.Model):
    STATUS_ON_TRACK = 'on_track'
    STATUS_AT_RISK = 'at_risk'
    STATUS_ACHIEVED = 'achieved'
    STATUS_CHOICES = [
        (STATUS_ON_TRACK, 'On Track'),
        (STATUS_AT_RISK, 'At Risk'),
        (STATUS_ACHIEVED, 'Achieved'),
    ]

    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    progress_percent = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ON_TRACK)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject


class SupportMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message on {self.ticket.subject}'
