from django import forms

from .models import JobApplication, Lead


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
