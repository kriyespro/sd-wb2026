from django import forms

from .models import DgcApplication, PartnerLead, PartnerOrder, PartnerProfile, ResellerOffer


class DgcApplicationForm(forms.ModelForm):
    class Meta:
        model = DgcApplication
        fields = ['name', 'email', 'phone', 'city', 'experience', 'why']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': '090235 61533',
            }),
            'city': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'City'}),
            'experience': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'Marketing / sales experience (years or summary)',
            }),
            'why': forms.Textarea(attrs={
                'class': 'wb-input', 'rows': 4,
                'placeholder': 'Why do you want to join as a DGC?',
            }),
        }


class PartnerOrderForm(forms.Form):
    offer = forms.ModelChoiceField(
        queryset=ResellerOffer.objects.none(),
        widget=forms.Select(attrs={'class': 'ops-select'}),
    )
    quantity = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={'class': 'ops-select', 'min': 1}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'ops-textarea', 'rows': 2, 'placeholder': 'Order notes (optional)',
        }),
    )

    def __init__(self, *args, **kwargs):
        offers = kwargs.pop('offers', None)
        super().__init__(*args, **kwargs)
        self.fields['offer'].queryset = offers if offers is not None else ResellerOffer.objects.filter(is_active=True)


class PartnerLeadForm(forms.ModelForm):
    class Meta:
        model = PartnerLead
        fields = ['name', 'phone', 'email', 'company', 'interest', 'notes', 'deal_value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Lead name'}),
            'phone': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'ops-select', 'placeholder': 'Email (optional)'}),
            'company': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Company'}),
            'interest': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Service interest'}),
            'notes': forms.Textarea(attrs={'class': 'ops-textarea', 'rows': 2, 'placeholder': 'Notes'}),
            'deal_value': forms.NumberInput(attrs={'class': 'ops-select', 'placeholder': '0', 'step': '0.01'}),
        }


class PartnerPayoutDetailsForm(forms.ModelForm):
    class Meta:
        model = PartnerProfile
        fields = ['upi_id', 'bank_account', 'bank_ifsc']
        widgets = {
            'upi_id': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'UPI ID'}),
            'bank_account': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'Bank account number'}),
            'bank_ifsc': forms.TextInput(attrs={'class': 'ops-select', 'placeholder': 'IFSC'}),
        }


class PartnerOrderStatusForm(forms.Form):
    status = forms.ChoiceField(choices=PartnerOrder.STATUS_CHOICES)


class PartnerLeadStatusForm(forms.Form):
    status = forms.ChoiceField(choices=PartnerLead.STATUS_CHOICES)
