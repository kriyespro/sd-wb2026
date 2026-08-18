from django import forms
from django.utils.text import slugify

from .models import JobApplication, JobOpening, Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'company', 'service_interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'wb-input',
                'placeholder': 'you@company.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': '+91 90235 61533',
            }),
            'company': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'Company name',
            }),
            'service_interest': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'e.g. SEO, Google Ads',
            }),
            'message': forms.Textarea(attrs={
                'class': 'wb-input',
                'rows': 4,
                'placeholder': 'Tell us about your goals...',
            }),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'name', 'email', 'phone', 'role', 'application_type',
            'experience', 'portfolio_url', 'linkedin_url', 'cover_letter',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'Full name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'wb-input',
                'placeholder': 'you@email.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': '+91 90235 61533',
                'required': True,
            }),
            'role': forms.Select(attrs={'class': 'wb-input', 'required': True}),
            'application_type': forms.Select(attrs={'class': 'wb-input'}),
            'experience': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'e.g. 2 years Meta Ads / Fresher',
            }),
            # TextInput — avoid browser type=url blocking submit on partial links
            'portfolio_url': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'https://your-portfolio.com (optional)',
            }),
            'linkedin_url': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'https://linkedin.com/in/you (optional)',
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'wb-input',
                'rows': 4,
                'placeholder': 'Why do you want this role? What have you built or shipped?',
                'required': True,
            }),
        }

    def __init__(self, *args, role_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = role_choices or []
        role_opts = [('', 'Select a role…')] + [(c, c) for c in choices]
        self.fields['role'].choices = role_opts
        self.fields['role'].widget.choices = role_opts
        # Optional URL fields — don't force Django URLField strictness on blank
        self.fields['portfolio_url'].required = False
        self.fields['linkedin_url'].required = False
        self.fields['experience'].required = False

    def _normalize_url(self, value):
        value = (value or '').strip()
        if not value:
            return ''
        if not value.startswith(('http://', 'https://')):
            value = 'https://' + value
        return value

    def clean_portfolio_url(self):
        return self._normalize_url(self.cleaned_data.get('portfolio_url'))

    def clean_linkedin_url(self):
        return self._normalize_url(self.cleaned_data.get('linkedin_url'))


def unique_job_opening_slug(title, exclude_pk=None):
    base = slugify(title)[:130] or 'role'
    slug = base
    n = 2
    qs = JobOpening.objects.all()
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    while qs.filter(slug=slug).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug


class JobOpeningForm(forms.ModelForm):
    """Ops-side add/edit — WB's own roles, and editing external submissions."""

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'ops-select',
            'placeholder': 'Comma separated, e.g. SEO, Content, Organic',
        }),
        help_text='Comma separated tags shown as chips on the careers card.',
    )

    class Meta:
        model = JobOpening
        fields = [
            'title', 'department', 'job_type', 'location', 'summary', 'tags', 'is_active',
            'company_name', 'contact_name', 'contact_email', 'contact_phone',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'e.g. Meta Ads Specialist'}),
            'department': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'e.g. Marketing'}),
            'job_type': forms.Select(attrs={'class': 'ops-select'}),
            'location': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'e.g. Surat / Hybrid'}),
            'summary': forms.Textarea(attrs={
                'class': 'ops-textarea', 'rows': 3,
                'placeholder': 'One or two sentences for the careers page card',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-slate-300 text-brand-600'}),
            'company_name': forms.TextInput(attrs={
                'class': 'ops-select', 'placeholder': 'Blank = posted as Winning Blueprints',
            }),
            'contact_name': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Optional'}),
            'contact_email': forms.EmailInput(attrs={'class': 'ops-select', 'placeholder': 'Optional'}),
            'contact_phone': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Optional'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join(self.instance.tags or [])
        for name in ['is_active', 'company_name', 'contact_name', 'contact_email', 'contact_phone']:
            self.fields[name].required = False

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        return [t.strip() for t in raw.split(',') if t.strip()]

    def save(self, commit=True):
        opening = super().save(commit=False)
        if not opening.slug:
            opening.slug = unique_job_opening_slug(opening.title, exclude_pk=opening.pk)
        if commit:
            opening.save()
        return opening


class JobPostSubmissionForm(forms.ModelForm):
    """Public 'post a job' form for outside companies — goes in pending until
    an admin reviews and approves it (see JobOpening.STATUS_PENDING)."""

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'wb-input',
            'placeholder': 'Comma separated, e.g. Remote, Design',
        }),
    )

    class Meta:
        model = JobOpening
        fields = [
            'company_name', 'contact_name', 'contact_email', 'contact_phone',
            'title', 'department', 'job_type', 'location', 'summary', 'tags',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Your company name'}),
            'contact_name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Your name'}),
            'contact_email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'you@company.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': '+91 90235 61533'}),
            'title': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Performance Marketer'}),
            'department': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Marketing'}),
            'job_type': forms.Select(attrs={'class': 'wb-input'}),
            'location': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Remote / Surat'}),
            'summary': forms.Textarea(attrs={
                'class': 'wb-input', 'rows': 4,
                'placeholder': 'What the role involves and who you are looking for',
            }),
        }

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        return [t.strip() for t in raw.split(',') if t.strip()]

    def save(self, commit=True):
        opening = super().save(commit=False)
        opening.status = JobOpening.STATUS_PENDING
        opening.is_active = False
        if not opening.slug:
            opening.slug = unique_job_opening_slug(opening.title, exclude_pk=opening.pk)
        if commit:
            opening.save()
        return opening
