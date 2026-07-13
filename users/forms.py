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


class PublicSignupForm(forms.Form):
    role = forms.ChoiceField(
        choices=PUBLIC_SIGNUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'signup-role'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'First name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Last name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'you@email.com'}),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Phone (optional)'}),
    )
    password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'wb-input', 'placeholder': 'Password (min 8)'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'wb-input', 'placeholder': 'Confirm password'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists. Please log in.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
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


class ChooseRoleForm(forms.Form):
    role = forms.ChoiceField(
        choices=PUBLIC_SIGNUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'signup-role'}),
    )
