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
    next_follow_up_at = models.DateTimeField(null=True, blank=True)
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

    @property
    def followup_progress(self):
        total = self.followups.count()
        if not total:
            return 0, 0
        done = self.followups.filter(is_done=True).count()
        return done, total


class LeadFollowUp(models.Model):
    """Office checklist steps for an inbound enquiry."""

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='followups')
    key = models.CharField(max_length=40)
    label = models.CharField(max_length=120)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)
    done_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_lead_followups',
    )
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['sort_order', 'id']
        unique_together = [('lead', 'key')]

    def __str__(self):
        return f'{self.lead_id}: {self.label}'


class JobApplication(models.Model):
    """Public careers / job applications (not Academy admissions)."""

    TYPE_FULLTIME = 'fulltime'
    TYPE_INTERNSHIP = 'internship'
    TYPE_CONTRACT = 'contract'
    TYPE_CHOICES = [
        (TYPE_FULLTIME, 'Full-time'),
        (TYPE_INTERNSHIP, 'Internship'),
        (TYPE_CONTRACT, 'Contract'),
    ]

    STATUS_NEW = 'new'
    STATUS_REVIEW = 'review'
    STATUS_INTERVIEW = 'interview'
    STATUS_HIRED = 'hired'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEW, 'Under Review'),
        (STATUS_INTERVIEW, 'Interview'),
        (STATUS_HIRED, 'Hired'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=120)
    application_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_FULLTIME,
    )
    experience = models.CharField(max_length=120, blank=True)
    portfolio_url = models.CharField(max_length=300, blank=True)
    linkedin_url = models.CharField(max_length=300, blank=True)
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.role}'
