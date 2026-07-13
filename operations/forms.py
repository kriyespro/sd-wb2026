from django import forms

from academy.models import MentorAllocation
from projects.models import Project
from users.roles import STUDENT_ROLES
from website.models import JobApplication, Lead

from .models import ProjectAssignment


class ProjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ['project', 'user', 'role', 'can_contact_client']
        widgets = {
            'project': forms.Select(attrs={'class': 'wb-input'}),
            'user': forms.Select(attrs={'class': 'wb-input'}),
            'role': forms.Select(attrs={'class': 'wb-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        user = cleaned.get('user')
        can_contact = cleaned.get('can_contact_client')
        # Students/interns may only contact clients when explicitly authorized.
        if user and hasattr(user, 'profile') and user.profile.role in STUDENT_ROLES:
            if can_contact:
                # Allowed only as an explicit override; keep it but flag intent is clear.
                pass
        return cleaned


class MentorAllocationForm(forms.ModelForm):
    class Meta:
        model = MentorAllocation
        fields = ['student', 'mentor', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'wb-input'}),
            'mentor': forms.Select(attrs={'class': 'wb-input'}),
            'notes': forms.Textarea(attrs={'class': 'wb-input', 'rows': 3}),
        }


class LeadStatusForm(forms.Form):
    status = forms.ChoiceField(choices=Lead.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'wb-input text-sm'}))


class LeadAssignForm(forms.Form):
    assigned_to = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Unassigned',
        widget=forms.Select(attrs={'class': 'wb-input text-sm'}),
    )

    def __init__(self, *args, **kwargs):
        from operations.lead_services import get_sales_executives
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_sales_executives()


class LeadNotesForm(forms.Form):
    handoff_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'wb-input text-sm', 'rows': 3, 'placeholder': 'Business consultant handoff notes…'}),
        required=False,
    )


class LeadConvertForm(forms.Form):
    project_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Project name (optional)'}),
    )


class JobApplicationStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=JobApplication.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'wb-input text-sm'}),
    )


class OrderAssignForm(forms.Form):
    assigned_to = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Unassigned',
        widget=forms.Select(attrs={'class': 'ops-select text-xs'}),
    )
    due_at = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'ops-select text-xs', 'type': 'date'}),
    )
    work_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'ops-textarea text-xs', 'rows': 2,
            'placeholder': 'Brief for developer / freelancer…',
        }),
    )

    def __init__(self, *args, **kwargs):
        from users.roles import DELIVERY_ROLES
        from django.contrib.auth.models import User
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(
            profile__role__in=DELIVERY_ROLES, is_active=True,
        ).select_related('profile')
