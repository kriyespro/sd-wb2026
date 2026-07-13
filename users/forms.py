from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .services import PUBLIC_SIGNUP_CHOICES, create_public_user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'wb-input',
            'placeholder': 'Email or username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'wb-input',
            'placeholder': 'Password',
        }),
    )


class ChooseRoleForm(forms.Form):
    role = forms.ChoiceField(
        choices=PUBLIC_SIGNUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'signup-role'}),
    )


# Kept for tests / admin provisioning helpers — not used on public signup UI.
class PublicSignupForm(forms.Form):
    role = forms.ChoiceField(choices=PUBLIC_SIGNUP_CHOICES)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    password1 = forms.CharField(min_length=8)
    password2 = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists. Please log in.')
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') and cleaned.get('password2') and cleaned['password1'] != cleaned['password2']:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned

    def save(self):
        return create_public_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            role=self.cleaned_data['role'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
            phone=self.cleaned_data.get('phone', ''),
        )
