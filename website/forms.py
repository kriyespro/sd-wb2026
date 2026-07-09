from django import forms

from .models import Lead


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
                'placeholder': '+91 98765 43210',
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
