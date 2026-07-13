import re

from django import forms

from .models import DgcApplication, PartnerLead, PartnerOrder, PartnerProfile, ResellerOffer

PAN_RE = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
IFSC_RE = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')


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


class PartnerKycForm(forms.ModelForm):
    """Full KYC profile after Google join — submitted for admin approval."""

    class Meta:
        model = DgcApplication
        fields = [
            'name', 'email', 'phone', 'city', 'address',
            'experience', 'why',
            'pan_number', 'aadhaar_last4',
            'upi_id', 'bank_account', 'bank_ifsc',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Full legal name'}),
            'email': forms.EmailInput(attrs={'class': 'wb-input', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'Mobile number'}),
            'city': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'City'}),
            'address': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': 'Full address (street, area, PIN)',
            }),
            'experience': forms.TextInput(attrs={
                'class': 'wb-input',
                'placeholder': 'Marketing / sales experience',
            }),
            'why': forms.Textarea(attrs={
                'class': 'wb-input', 'rows': 4,
                'placeholder': 'Why do you want to join as a DGC?',
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': 'PAN number', 'style': 'text-transform:uppercase',
            }),
            'aadhaar_last4': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': 'Last 4 digits of Aadhaar', 'maxlength': '4',
            }),
            'upi_id': forms.TextInput(attrs={'class': 'wb-input', 'placeholder': 'UPI ID'}),
            'bank_account': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': 'Bank account number',
            }),
            'bank_ifsc': forms.TextInput(attrs={
                'class': 'wb-input', 'placeholder': 'IFSC code', 'style': 'text-transform:uppercase',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['address'].required = True
        self.fields['phone'].required = True
        self.fields['experience'].required = True
        self.fields['pan_number'].required = True
        if user and user.email and not self.initial.get('email'):
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True
        if user and user.get_full_name() and not self.initial.get('name'):
            self.fields['name'].initial = user.get_full_name()

    def clean_pan_number(self):
        pan = (self.cleaned_data.get('pan_number') or '').strip().upper()
        if pan and not PAN_RE.match(pan):
            raise forms.ValidationError('Enter a valid PAN (e.g. ABCDE1234F).')
        return pan

    def clean_aadhaar_last4(self):
        val = (self.cleaned_data.get('aadhaar_last4') or '').strip()
        if val and (len(val) != 4 or not val.isdigit()):
            raise forms.ValidationError('Enter exactly 4 digits.')
        return val

    def clean_bank_ifsc(self):
        ifsc = (self.cleaned_data.get('bank_ifsc') or '').strip().upper()
        if ifsc and not IFSC_RE.match(ifsc):
            raise forms.ValidationError('Enter a valid IFSC code (e.g. HDFC0001234).')
        return ifsc

    def clean_bank_account(self):
        val = re.sub(r'\s+', '', self.cleaned_data.get('bank_account') or '')
        if val and not val.isdigit():
            raise forms.ValidationError('Bank account number should contain digits only.')
        return val


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

    def clean_bank_ifsc(self):
        ifsc = (self.cleaned_data.get('bank_ifsc') or '').strip().upper()
        if ifsc and not IFSC_RE.match(ifsc):
            raise forms.ValidationError('Enter a valid IFSC code (e.g. HDFC0001234).')
        return ifsc

    def clean_bank_account(self):
        val = re.sub(r'\s+', '', self.cleaned_data.get('bank_account') or '')
        if val and not val.isdigit():
            raise forms.ValidationError('Bank account number should contain digits only.')
        return val


class PartnerOrderStatusForm(forms.Form):
    status = forms.ChoiceField(choices=PartnerOrder.STATUS_CHOICES)


class PartnerLeadStatusForm(forms.Form):
    status = forms.ChoiceField(choices=PartnerLead.STATUS_CHOICES)
