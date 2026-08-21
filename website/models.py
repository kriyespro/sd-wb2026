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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.role}'


class JobOpening(models.Model):
    """Public /careers/ job listings — Winning Blueprints roles added directly
    by ops, plus external company postings that sit pending until approved."""

    TYPE_FULLTIME = 'Full-time'
    TYPE_INTERNSHIP = 'Internship'
    TYPE_CONTRACT = 'Contract'
    TYPE_CHOICES = [
        (TYPE_FULLTIME, 'Full-time'),
        (TYPE_INTERNSHIP, 'Internship'),
        (TYPE_CONTRACT, 'Contract'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    department = models.CharField(max_length=80)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_FULLTIME)
    location = models.CharField(max_length=120, default='Surat / Hybrid')
    summary = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_APPROVED, db_index=True,
    )
    # Set for postings submitted by an outside company — blank for WB's own roles.
    company_name = models.CharField(max_length=120, blank=True)
    contact_name = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department', 'title']

    def __str__(self):
        return self.title

    @property
    def is_external(self):
        return bool(self.company_name)


class TitleDescBlock(models.Model):
    """Small reusable card content (title/desc/icon/image/badge) shown in
    grouped lists across public pages. `section` tags which page/list a row
    belongs to so each view queries just its own slice, ordered by `order`.
    Replaces the simple title+desc-shaped constants in website/data.py."""

    SECTION_WHY_CHOOSE_US = 'why_choose_us'
    SECTION_STARTUP_PROMISES = 'startup_promises'
    SECTION_STARTUP_FOR = 'startup_for'
    SECTION_F2C_PIPELINE = 'f2c_pipeline'
    SECTION_MODEL_STEPS = 'model_steps'
    SECTION_INDUSTRIES = 'industries'
    SECTION_TEAM_DEPARTMENTS = 'team_departments'
    SECTION_TEAM_ROLES = 'team_roles'
    SECTION_CAREERS_PERKS = 'careers_perks'
    SECTION_ACADEMY_PROCESS = 'academy_process'
    SECTION_AUDIENCE_TAGS = 'audience_tags'
    SECTION_HERO_POINTS = 'hero_points'
    SECTION_CHOICES = [
        (SECTION_WHY_CHOOSE_US, 'Why Choose Us (home / services / about)'),
        (SECTION_STARTUP_PROMISES, 'Startup Plan — Promises'),
        (SECTION_STARTUP_FOR, "Startup Plan — Who it's for"),
        (SECTION_F2C_PIPELINE, 'Factory-to-Customer Pipeline (home / services)'),
        (SECTION_MODEL_STEPS, 'Dual Model steps (home / about)'),
        (SECTION_INDUSTRIES, 'Industries served'),
        (SECTION_TEAM_DEPARTMENTS, 'Team — Departments'),
        (SECTION_TEAM_ROLES, 'Team — Capacity by role'),
        (SECTION_CAREERS_PERKS, 'Careers — Perks'),
        (SECTION_ACADEMY_PROCESS, 'Careers — Academy process steps'),
        (SECTION_AUDIENCE_TAGS, 'Home — Audience tags'),
        (SECTION_HERO_POINTS, 'Home — Hero bullet points'),
    ]

    section = models.CharField(max_length=30, choices=SECTION_CHOICES, db_index=True)
    title = models.CharField(max_length=160, blank=True)
    desc = models.TextField(blank=True)
    icon = models.CharField(max_length=20, blank=True, help_text='Emoji, e.g. 🏭')
    image = models.URLField(max_length=500, blank=True)
    badge = models.CharField(max_length=20, blank=True, help_text='Short label, e.g. a headcount like "25"')
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['section', 'order', 'id']

    def __str__(self):
        return f'{self.get_section_display()}: {self.title}'


class StatBlock(models.Model):
    """Home/about/team/startup/careers stat strip (e.g. "12+ Years Experience")."""

    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True)
    label = models.CharField(max_length=80)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.value}{self.suffix} {self.label}'


class ProjectBlock(models.Model):
    """Recent-projects cards shown on home / services / our-work / careers / join."""

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=80)
    result = models.CharField(max_length=160)
    image = models.URLField(max_length=500, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    initials = models.CharField(max_length=6, blank=True)
    photo = models.URLField(max_length=500, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.name} — {self.role}'


class FAQ(models.Model):
    GROUP_PRICING = 'pricing'
    GROUP_GENERAL = 'general'
    GROUP_STARTUP = 'startup'
    GROUP_LP_AI_DM = 'lp_ai_dm'
    GROUP_CHOICES = [
        (GROUP_PRICING, 'Pricing page'),
        (GROUP_GENERAL, 'General (home / pricing)'),
        (GROUP_STARTUP, 'Startup Plan page'),
        (GROUP_LP_AI_DM, 'Digital Launchpad landing page'),
    ]

    group = models.CharField(max_length=20, choices=GROUP_CHOICES, db_index=True)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['group', 'order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class TeamMember(models.Model):
    """Unifies the old TEAM_FOUNDERS + TEAM_CORE constants — `is_founder`
    replaces having two separate lists."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=160)
    tags = models.JSONField(default=list, blank=True)
    initials = models.CharField(max_length=6, blank=True)
    bio = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True)
    image_upload = models.FileField(upload_to='team/', blank=True, help_text='Uploading a photo here overrides the Image URL above.')
    is_founder = models.BooleanField(default=False, db_index=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_founder', 'order', 'id']

    def __str__(self):
        return f'{self.name} — {self.role}'


class Service(models.Model):
    """Public /services/ catalog. `is_flagship` rows also show as one of the
    3 home-page flagship package cards (replaces FLAGSHIP_OFFERS, which
    always linked to a SERVICES row by slug anyway)."""

    slug = models.SlugField(max_length=140, unique=True)
    title = models.CharField(max_length=160)
    icon = models.CharField(max_length=20, blank=True)
    short = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    gallery = models.JSONField(default=list, blank=True)
    is_flagship = models.BooleanField(default=False, db_index=True)
    flagship_features = models.JSONField(default=list, blank=True)
    popular = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    slug = models.SlugField(max_length=140, unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=120)
    client = models.CharField(max_length=160)
    result = models.CharField(max_length=200)
    summary = models.TextField()
    image = models.URLField(max_length=500, blank=True)
    impact_areas = models.JSONField(default=list, blank=True)
    gallery = models.JSONField(default=list, blank=True)
    narrative = models.JSONField(default=list, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Case studies'

    def __str__(self):
        return self.title


class PricingTier(models.Model):
    name = models.CharField(max_length=80)
    price = models.CharField(max_length=40)
    price_monthly = models.CharField(max_length=40, blank=True)
    price_annual = models.CharField(max_length=40, blank=True)
    period = models.CharField(max_length=20, blank=True)
    features = models.JSONField(default=list, blank=True)
    highlight = models.BooleanField(default=False)
    blurb = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class StartupPhase(models.Model):
    num = models.CharField(max_length=4)
    slug = models.SlugField(max_length=60, unique=True)
    short = models.CharField(max_length=40)
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=200, blank=True)
    desc = models.TextField(blank=True)
    outcomes = models.JSONField(default=list, blank=True)
    duration = models.CharField(max_length=60, blank=True)
    icon = models.CharField(max_length=20, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Single-row settings for site-wide images + contact info, edited via
    /ops/cms/site-settings/ — no add/delete, just one row (pk=1)."""

    hero_image = models.URLField(max_length=500, blank=True)
    contact_bg_image = models.URLField(max_length=500, blank=True)
    about_team_image = models.URLField(max_length=500, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_address = models.CharField(max_length=300, blank=True)
    contact_hours = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
