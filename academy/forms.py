from django import forms

from .models import (
    ActivityLog,
    AdmissionApplication,
    PortfolioItem,
    StudentLead,
    StudentProject,
    Submission,
    TeachingSession,
)


class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['name', 'email', 'phone', 'education', 'course_interest', 'motivation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'you@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': '+91 90235 61533'}),
            'education': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. B.Com, BBA'}),
            'course_interest': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Digital Marketing'}),
            'motivation': forms.Textarea(attrs={'class': 'wb-input', 'rows': 4, 'placeholder': 'Why do you want to join?'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'wb-input', 'rows': 4, 'placeholder': 'Your submission...',
            }),
        }


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'project_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Project title'}),
            'description': forms.Textarea(attrs={'class': 'wb-input', 'rows': 3, 'placeholder': 'Describe the project'}),
            'project_url': forms.URLInput(attrs={'class': 'wb-input', 'placeholder': 'https://...'}),
        }


class TeachingSessionForm(forms.ModelForm):
    class Meta:
        model = TeachingSession
        fields = ['topic', 'explanation', 'resource_url']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Canonical tags'}),
            'explanation': forms.Textarea(attrs={
                'class': 'wb-input', 'rows': 4, 'placeholder': 'Explain what you taught and how...',
            }),
            'resource_url': forms.URLInput(attrs={'class': 'wb-input', 'placeholder': 'Recording / deck link (optional)'}),
        }


class TeachingEvaluationForm(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=100, widget=forms.NumberInput(attrs={'class': 'wb-input'}))
    feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'wb-input', 'rows': 2, 'placeholder': 'Feedback (optional)'}),
    )


class StudentLeadForm(forms.ModelForm):
    class Meta:
        model = StudentLead
        fields = ['business_name', 'contact_name', 'phone', 'email', 'interest', 'notes', 'deal_value']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Business name'}),
            'contact_name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Contact person'}),
            'phone': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'Email'}),
            'interest': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'e.g. Website, SEO'}),
            'notes': forms.Textarea(attrs={'class': 'wb-input', 'rows': 2, 'placeholder': 'Notes'}),
            'deal_value': forms.NumberInput(attrs={'class': 'wb-input', 'placeholder': '0'}),
        }


class StudentLeadStatusForm(forms.Form):
    status = forms.ChoiceField(choices=StudentLead.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'wb-input'}))


class DailyFourDForm(forms.Form):
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'wb-input', 'rows': 3, 'placeholder': "Today's reflection (optional)",
        }),
    )


class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['pillar', 'title', 'details']
        widgets = {
            'pillar': forms.Select(attrs={'class': 'wb-input'}),
            'title': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'What did you do?'}),
            'details': forms.Textarea(attrs={'class': 'wb-input', 'rows': 2, 'placeholder': 'Details (optional)'}),
        }


class StudentProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ['client_name', 'project_value', 'payment_status', 'revenue_collected']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Client name'}),
            'project_value': forms.NumberInput(attrs={'class': 'wb-input', 'placeholder': '0'}),
            'payment_status': forms.Select(attrs={'class': 'wb-input'}),
            'revenue_collected': forms.NumberInput(attrs={'class': 'wb-input', 'placeholder': '0'}),
        }
