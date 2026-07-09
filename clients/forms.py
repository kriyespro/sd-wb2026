from django import forms

from .models import SupportTicket


class SupportTicketForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Subject'}),
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'wb-input', 'rows': 4, 'placeholder': 'How can we help?'}),
    )


class TicketReplyForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'wb-input', 'rows': 3, 'placeholder': 'Write a reply...'}),
    )
