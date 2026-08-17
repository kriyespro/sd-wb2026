from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField(default=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Lesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_DROPPED = 'dropped'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_DROPPED, 'Dropped'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    progress_percent = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user.username} — {self.course.title}'


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title


class Submission(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SUBMITTED = 'submitted'
    STATUS_REVIEWED = 'reviewed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_REVIEWED, 'Reviewed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SUBMITTED)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'assignment']
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.user.username} — {self.assignment.title}'


class StudentTask(models.Model):
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    ]

    STAGE_GENERAL = 'general'
    STAGE_LEARN = 'learn'
    STAGE_TEACH = 'teach'
    STAGE_FIELD = 'field'
    STAGE_EARN = 'earn'
    STAGE_CHOICES = [
        (STAGE_GENERAL, 'General'),
        (STAGE_LEARN, 'Learn'),
        (STAGE_TEACH, 'Teach'),
        (STAGE_FIELD, 'Field'),
        (STAGE_EARN, 'Earn'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default=STAGE_GENERAL)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tasks_assigned',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return self.title


class StudentProject(models.Model):
    TYPE_MOCK = 'mock'
    TYPE_INTERNAL = 'internal'
    TYPE_REAL = 'real'
    TYPE_CHOICES = [
        (TYPE_MOCK, 'Mock Project'),
        (TYPE_INTERNAL, 'Internal Project'),
        (TYPE_REAL, 'Real Client Project'),
    ]
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    PAYMENT_UNPAID = 'unpaid'
    PAYMENT_PARTIAL = 'partial'
    PAYMENT_PAID = 'paid'
    PAYMENT_CHOICES = [
        (PAYMENT_UNPAID, 'Unpaid'),
        (PAYMENT_PARTIAL, 'Partially Paid'),
        (PAYMENT_PAID, 'Paid'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_MOCK)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    client_name = models.CharField(max_length=200, blank=True)
    project_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MentorAllocation(models.Model):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_allocation',
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentees',
    )
    notes = models.TextField(blank=True)
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} → {self.mentor.username}'


class Attendance(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_LATE = 'late'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    session_name = models.CharField(max_length=200)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PRESENT)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'session_name', 'date']

    def __str__(self):
        return f'{self.user.username} — {self.date}'


class PortfolioItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    issued_at = models.DateField()

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return self.title


class PlacementApplication(models.Model):
    STATUS_APPLIED = 'applied'
    STATUS_INTERVIEW = 'interview'
    STATUS_OFFERED = 'offered'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_APPLIED, 'Applied'),
        (STATUS_INTERVIEW, 'Interview'),
        (STATUS_OFFERED, 'Offered'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placement_applications')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.company} — {self.role}'


class TeachingSession(models.Model):
    STATUS_SUBMITTED = 'submitted'
    STATUS_EVALUATED = 'evaluated'
    STATUS_CHOICES = [
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_EVALUATED, 'Evaluated'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teaching_sessions')
    topic = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)
    resource_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SUBMITTED, db_index=True)
    evaluated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='teaching_evaluations',
    )
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.topic}'


class StudentLead(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_INTERESTED = 'interested'
    STATUS_WON = 'won'
    STATUS_LOST = 'lost'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_INTERESTED, 'Interested'),
        (STATUS_WON, 'Won'),
        (STATUS_LOST, 'Lost'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='field_leads')
    business_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    interest = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    deal_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.business_name} — {self.get_status_display()}'


class DailyFourD(models.Model):
    """The student's daily reflection record. Pillar completion and score are
    always derived live from Submission/TeachingSession/StudentLead/StudentTask
    evidence (see academy.fourd_services) — this model only stores the notes,
    so nothing here can drift out of sync with what actually happened."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_fourd_logs')
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} — {self.date}'


class ActivityLog(models.Model):
    """A student's own free-form record of what they did for a pillar today.
    Purely descriptive — never read by fourd_services.pillar_status/daily_score,
    so it can't be used to fake evidence-based scoring. Exists so progress
    tracking has a human narrative alongside the structured evidence."""

    PILLAR_LEARN = 'learn'
    PILLAR_TEACH = 'teach'
    PILLAR_FIELD = 'field'
    PILLAR_EARN = 'earn'
    PILLAR_CHOICES = [
        (PILLAR_LEARN, 'Learn'),
        (PILLAR_TEACH, 'Teach'),
        (PILLAR_FIELD, 'Field'),
        (PILLAR_EARN, 'Earn'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f'{self.user.username} — {self.title}'


class AdmissionApplication(models.Model):
    STATUS_NEW = 'new'
    STATUS_REVIEW = 'review'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEW, 'Under Review'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=200)
    course_interest = models.CharField(max_length=200, blank=True)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    razorpay_order_id = models.CharField(max_length=64, blank=True)
    razorpay_payment_id = models.CharField(max_length=64, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.email}'
