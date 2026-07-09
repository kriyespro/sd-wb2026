from django import forms

from .models import AdmissionApplication, PortfolioItem, Submission


class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['name', 'email', 'phone', 'education', 'course_interest', 'motivation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'you@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': '+91 98765 43210'}),
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
