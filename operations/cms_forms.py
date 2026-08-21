"""ModelForms for the /ops/cms/ public-site content editor. List/JSON
fields are edited as plain line-based text and parsed back into the
model's list/JSON structure on save — same pattern as CourseListingForm
in academy/forms.py."""

from django import forms

from core.form_utils import lines_to_list, list_to_lines
from website.models import (
    CaseStudy,
    FAQ,
    PricingTier,
    ProjectBlock,
    Service,
    SiteSettings,
    StartupPhase,
    StatBlock,
    TeamMember,
    Testimonial,
    TitleDescBlock,
)

_TEXT = {'class': 'ops-select text-base py-2.5 border-slate-300'}
_TEXTAREA = {'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 3, 'placeholder': 'One per line'}
_CHECK = {'class': 'h-4 w-4 rounded border-slate-300 text-brand-600'}


def _parse_narrative(text):
    sections = []
    for line in (text or '').splitlines():
        line = line.strip()
        if not line:
            continue
        heading, _, body = line.partition('|')
        sections.append({'heading': heading.strip(), 'body': body.strip()})
    return sections


def _narrative_to_text(sections):
    return '\n'.join(f"{s.get('heading', '')} | {s.get('body', '')}" for s in sections or [])


class ListFieldFormMixin:
    """For forms whose `list_fields` are declared as plain CharField+Textarea
    (overriding the model's JSONField widget, same as CourseListingForm) —
    populates textarea initial text from the model's list on edit, and
    `_clean_list_field` converts the textarea text back to a list on save."""

    list_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            for name in self.list_fields:
                self.fields[name].initial = list_to_lines(getattr(self.instance, name))

    def _clean_list_field(self, name):
        return lines_to_list(self.cleaned_data.get(name))


class TitleDescBlockForm(forms.ModelForm):
    class Meta:
        model = TitleDescBlock
        fields = ['section', 'title', 'desc', 'icon', 'image', 'badge', 'order', 'is_active']
        widgets = {
            'section': forms.Select(attrs=_TEXT),
            'title': forms.TextInput(attrs=_TEXT),
            'desc': forms.Textarea(attrs={**_TEXTAREA, 'rows': 2, 'placeholder': ''}),
            'icon': forms.TextInput(attrs={**_TEXT, 'placeholder': 'Emoji (optional)'}),
            'image': forms.URLInput(attrs={**_TEXT, 'placeholder': 'https://... (optional)'}),
            'badge': forms.TextInput(attrs={**_TEXT, 'placeholder': 'e.g. 25 (optional)'}),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }


class StatBlockForm(forms.ModelForm):
    class Meta:
        model = StatBlock
        fields = ['value', 'suffix', 'label', 'order', 'is_active']
        widgets = {
            'value': forms.NumberInput(attrs=_TEXT),
            'suffix': forms.TextInput(attrs={**_TEXT, 'placeholder': 'e.g. +, x, %'}),
            'label': forms.TextInput(attrs=_TEXT),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }


class ProjectBlockForm(forms.ModelForm):
    class Meta:
        model = ProjectBlock
        fields = ['title', 'category', 'result', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs=_TEXT),
            'category': forms.TextInput(attrs=_TEXT),
            'result': forms.TextInput(attrs=_TEXT),
            'image': forms.URLInput(attrs=_TEXT),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['quote', 'name', 'role', 'company', 'initials', 'photo', 'order', 'is_active']
        widgets = {
            'quote': forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': ''}),
            'name': forms.TextInput(attrs=_TEXT),
            'role': forms.TextInput(attrs=_TEXT),
            'company': forms.TextInput(attrs=_TEXT),
            'initials': forms.TextInput(attrs=_TEXT),
            'photo': forms.URLInput(attrs={**_TEXT, 'placeholder': 'https://... (optional)'}),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['group', 'question', 'answer', 'order', 'is_active']
        widgets = {
            'group': forms.Select(attrs=_TEXT),
            'question': forms.TextInput(attrs=_TEXT),
            'answer': forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': ''}),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }


class TeamMemberForm(ListFieldFormMixin, forms.ModelForm):
    list_fields = ['tags']
    tags = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 2}))

    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'tags', 'initials', 'bio', 'image', 'image_upload', 'is_founder', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs=_TEXT),
            'role': forms.TextInput(attrs=_TEXT),
            'initials': forms.TextInput(attrs=_TEXT),
            'bio': forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': ''}),
            'image': forms.URLInput(attrs={**_TEXT, 'placeholder': 'https://... (optional)'}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'accept': 'image/*'}),
            'is_founder': forms.CheckboxInput(attrs=_CHECK),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_upload'].required = False

    def clean_tags(self):
        return self._clean_list_field('tags')

    def save(self, commit=True):
        member = super().save(commit=False)
        if commit:
            member.save()
            if member.image_upload:
                new_image = member.image_upload.url
                if member.image != new_image:
                    member.image = new_image
                    member.save(update_fields=['image'])
        return member


class ServiceForm(ListFieldFormMixin, forms.ModelForm):
    list_fields = ['gallery', 'flagship_features']
    gallery = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': 'One image URL per line'}))
    flagship_features = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 3}))

    class Meta:
        model = Service
        fields = [
            'slug', 'title', 'icon', 'short', 'description', 'gallery',
            'is_flagship', 'flagship_features', 'popular', 'order', 'is_active',
        ]
        widgets = {
            'slug': forms.TextInput(attrs={**_TEXT, 'placeholder': 'auto-filled if left blank'}),
            'title': forms.TextInput(attrs=_TEXT),
            'icon': forms.TextInput(attrs={**_TEXT, 'placeholder': 'Emoji'}),
            'short': forms.TextInput(attrs=_TEXT),
            'description': forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': ''}),
            'is_flagship': forms.CheckboxInput(attrs=_CHECK),
            'popular': forms.CheckboxInput(attrs=_CHECK),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_gallery(self):
        return self._clean_list_field('gallery')

    def clean_flagship_features(self):
        return self._clean_list_field('flagship_features')

    def save(self, commit=True):
        from django.utils.text import slugify
        service = super().save(commit=False)
        if not service.slug:
            service.slug = slugify(service.title)[:130] or 'service'
        if commit:
            service.save()
        return service


class CaseStudyForm(ListFieldFormMixin, forms.ModelForm):
    list_fields = ['impact_areas', 'gallery']
    impact_areas = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 3}))
    gallery = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': 'One image URL per line'}))
    narrative = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 5, 'placeholder': 'The Challenge | body text\nThe Approach | body text\nThe Result | body text'}),
        help_text='One section per line: Heading | Body',
    )

    class Meta:
        model = CaseStudy
        fields = [
            'slug', 'title', 'category', 'client', 'result', 'summary', 'image',
            'impact_areas', 'gallery', 'narrative', 'order', 'is_active',
        ]
        widgets = {
            'slug': forms.TextInput(attrs={**_TEXT, 'placeholder': 'auto-filled if left blank'}),
            'title': forms.TextInput(attrs=_TEXT),
            'category': forms.TextInput(attrs=_TEXT),
            'client': forms.TextInput(attrs=_TEXT),
            'result': forms.TextInput(attrs=_TEXT),
            'summary': forms.Textarea(attrs={**_TEXTAREA, 'rows': 2, 'placeholder': ''}),
            'image': forms.URLInput(attrs=_TEXT),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        if self.instance and self.instance.pk:
            self.fields['narrative'].initial = _narrative_to_text(self.instance.narrative)

    def clean_impact_areas(self):
        return self._clean_list_field('impact_areas')

    def clean_gallery(self):
        return self._clean_list_field('gallery')

    def clean_narrative(self):
        return _parse_narrative(self.cleaned_data.get('narrative'))

    def save(self, commit=True):
        from django.utils.text import slugify
        study = super().save(commit=False)
        if not study.slug:
            study.slug = slugify(study.title)[:130] or 'case-study'
        if commit:
            study.save()
        return study


class PricingTierForm(ListFieldFormMixin, forms.ModelForm):
    list_fields = ['features']
    features = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 4}))

    class Meta:
        model = PricingTier
        fields = [
            'name', 'price', 'price_monthly', 'price_annual', 'period',
            'features', 'highlight', 'blurb', 'order', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs=_TEXT),
            'price': forms.TextInput(attrs=_TEXT),
            'price_monthly': forms.TextInput(attrs=_TEXT),
            'price_annual': forms.TextInput(attrs=_TEXT),
            'period': forms.TextInput(attrs={**_TEXT, 'placeholder': 'e.g. /month'}),
            'highlight': forms.CheckboxInput(attrs=_CHECK),
            'blurb': forms.TextInput(attrs=_TEXT),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }

    def clean_features(self):
        return self._clean_list_field('features')


class StartupPhaseForm(ListFieldFormMixin, forms.ModelForm):
    list_fields = ['outcomes']
    outcomes = forms.CharField(required=False, widget=forms.Textarea(attrs={**_TEXTAREA, 'rows': 4}))

    class Meta:
        model = StartupPhase
        fields = [
            'num', 'slug', 'short', 'title', 'subtitle', 'desc',
            'outcomes', 'duration', 'icon', 'order', 'is_active',
        ]
        widgets = {
            'num': forms.TextInput(attrs={**_TEXT, 'placeholder': 'e.g. 01'}),
            'slug': forms.TextInput(attrs={**_TEXT, 'placeholder': 'auto-filled if left blank'}),
            'short': forms.TextInput(attrs=_TEXT),
            'title': forms.TextInput(attrs=_TEXT),
            'subtitle': forms.TextInput(attrs=_TEXT),
            'desc': forms.Textarea(attrs={**_TEXTAREA, 'rows': 3, 'placeholder': ''}),
            'duration': forms.TextInput(attrs={**_TEXT, 'placeholder': 'e.g. 4–10 weeks'}),
            'icon': forms.TextInput(attrs={**_TEXT, 'placeholder': 'Emoji'}),
            'order': forms.NumberInput(attrs=_TEXT),
            'is_active': forms.CheckboxInput(attrs=_CHECK),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_outcomes(self):
        return self._clean_list_field('outcomes')

    def save(self, commit=True):
        from django.utils.text import slugify
        phase = super().save(commit=False)
        if not phase.slug:
            phase.slug = slugify(phase.title)[:55] or 'phase'
        if commit:
            phase.save()
        return phase


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'hero_image', 'contact_bg_image', 'about_team_image',
            'contact_email', 'contact_phone', 'contact_address', 'contact_hours',
        ]
        widgets = {
            'hero_image': forms.URLInput(attrs=_TEXT),
            'contact_bg_image': forms.URLInput(attrs=_TEXT),
            'about_team_image': forms.URLInput(attrs=_TEXT),
            'contact_email': forms.EmailInput(attrs=_TEXT),
            'contact_phone': forms.TextInput(attrs=_TEXT),
            'contact_address': forms.TextInput(attrs=_TEXT),
            'contact_hours': forms.TextInput(attrs=_TEXT),
        }
