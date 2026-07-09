from django.conf import settings
from django.db import models

from projects.models import Project


class Team(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    SENIORITY_SENIOR = 'senior'
    SENIORITY_EXECUTIVE = 'executive'
    SENIORITY_INTERN = 'intern'
    SENIORITY_STUDENT = 'student'
    SENIORITY_CHOICES = [
        (SENIORITY_SENIOR, 'Senior'),
        (SENIORITY_EXECUTIVE, 'Executive'),
        (SENIORITY_INTERN, 'Intern'),
        (SENIORITY_STUDENT, 'Student'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_memberships')
    seniority = models.CharField(max_length=20, choices=SENIORITY_CHOICES, default=SENIORITY_EXECUTIVE)

    class Meta:
        unique_together = ['team', 'user']
        ordering = ['seniority']

    def __str__(self):
        return f'{self.user.username} — {self.team.name}'


class ProjectAssignment(models.Model):
    ROLE_PM = 'pm'
    ROLE_SENIOR = 'senior'
    ROLE_EXECUTIVE = 'executive'
    ROLE_INTERN = 'intern'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = [
        (ROLE_PM, 'Project Manager'),
        (ROLE_SENIOR, 'Senior Specialist'),
        (ROLE_EXECUTIVE, 'Executive'),
        (ROLE_INTERN, 'Intern'),
        (ROLE_STUDENT, 'Student'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_assignments')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EXECUTIVE)
    # Students/interns cannot contact clients unless explicitly authorized.
    can_contact_client = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']
        ordering = ['role']

    def __str__(self):
        return f'{self.user.username} — {self.project.name} ({self.get_role_display()})'


class Assessment(models.Model):
    STATUS_SCHEDULED = 'scheduled'
    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_PASSED, 'Passed'),
        (STATUS_FAILED, 'Failed'),
    ]

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200)
    score = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.candidate.username} — {self.title}'


class PerformanceReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviews_given',
    )
    period = models.CharField(max_length=120)
    rating = models.PositiveIntegerField(default=3, help_text='1-5')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.period}'
