from django import forms
from django.utils.text import slugify

from .models import (
    ActivityLog,
    AdmissionApplication,
    CourseListing,
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


def unique_course_slug(title, exclude_pk=None):
    base = slugify(title)[:130] or 'course'
    slug = base
    n = 2
    qs = CourseListing.objects.all()
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    while qs.filter(slug=slug).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug


def _lines_to_list(text):
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


def _list_to_lines(items):
    return '\n'.join(items or [])


def _parse_curriculum(text):
    modules = []
    for line in (text or '').splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        title = parts[0].strip()
        free = len(parts) > 1 and parts[1].strip().lower() in ('free', 'yes', 'true', '1')
        topics_raw = parts[2] if len(parts) > 2 else ''
        topics = [t.strip() for t in topics_raw.split(';') if t.strip()]
        modules.append({'title': title, 'topics': topics, 'free_preview': free})
    return modules


def _curriculum_to_text(modules):
    lines = []
    for m in modules or []:
        free = 'free' if m.get('free_preview') else ''
        topics = '; '.join(m.get('topics') or [])
        lines.append(f"{m.get('title', '')} | {free} | {topics}")
    return '\n'.join(lines)


def _parse_reviews(text):
    reviews = []
    for line in (text or '').splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split('|')]
        parts += [''] * (4 - len(parts))
        quote, name, role, city = parts[:4]
        reviews.append({'quote': quote, 'name': name, 'role': role, 'city': city})
    return reviews


def _reviews_to_text(reviews):
    lines = []
    for r in reviews or []:
        lines.append(f"{r.get('quote', '')} | {r.get('name', '')} | {r.get('role', '')} | {r.get('city', '')}")
    return '\n'.join(lines)


class CourseListingForm(forms.ModelForm):
    """Ops-side add/edit for the public /academy/courses/ catalog. The
    nested/list fields (curriculum, reviews, gains, ...) are edited as plain
    line-based text and parsed into the model's JSON structure on save —
    no nested formset builder, matches what the user asked for."""

    gains = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 4, 'placeholder': 'One per line',
    }))
    includes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 4, 'placeholder': 'One per line',
    }))
    learn_modules = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 4, 'placeholder': 'One per line',
    }))
    ideal_paths = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 3, 'placeholder': 'One per line',
    }))
    overview = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 5, 'placeholder': 'One paragraph per line',
    }))
    curriculum = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 8,
            'placeholder': 'Module Title | free | topic1; topic2; topic3\nAnother Module | | topic1; topic2',
        }),
        help_text='One module per line: Title | free (write "free" for a preview module, else blank) | topics separated by ;',
    )
    reviews = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 5, 'placeholder': 'Quote | Name | Role | City',
        }),
        help_text='One review per line: Quote | Name | Role | City',
    )

    class Meta:
        model = CourseListing
        fields = [
            'title', 'goal', 'level', 'duration', 'format', 'modules_count', 'topics_count',
            'price', 'salary_range', 'featured', 'enrolled', 'rating', 'reviews_count', 'image',
            'gains', 'includes', 'learn_modules', 'ideal_paths', 'overview', 'curriculum', 'reviews',
            'career_label', 'career_min', 'career_max', 'highlight_quote', 'highlight_author',
            'starts_with', 'is_active', 'sort_order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. AI Automation Engineering Pro'}),
            'goal': forms.Textarea(attrs={'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 3, 'placeholder': 'One or two sentence course goal'}),
            'level': forms.Select(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'duration': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. 12 weeks'}),
            'format': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. Self-paced'}),
            'modules_count': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'topics_count': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'price': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. ₹16,999'}),
            'salary_range': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. ₹4–12 LPA (optional)'}),
            'enrolled': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'rating': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'step': '0.1'}),
            'reviews_count': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'image': forms.URLInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'https://... (course card image)'}),
            'career_label': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. Entry to senior roles'}),
            'career_min': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. ₹3L'}),
            'career_max': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. ₹12L'}),
            'highlight_quote': forms.Textarea(attrs={'class': 'ops-textarea text-base py-2.5 border-slate-300 leading-relaxed', 'rows': 2, 'placeholder': 'Short testimonial quote'}),
            'highlight_author': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'e.g. Name, Role'}),
            'starts_with': forms.TextInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300', 'placeholder': 'First module title'}),
            'sort_order': forms.NumberInput(attrs={'class': 'ops-select text-base py-2.5 border-slate-300'}),
            'featured': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-slate-300 text-brand-600'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-slate-300 text-brand-600'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['gains'].initial = _list_to_lines(self.instance.gains)
            self.fields['includes'].initial = _list_to_lines(self.instance.includes)
            self.fields['learn_modules'].initial = _list_to_lines(self.instance.learn_modules)
            self.fields['ideal_paths'].initial = _list_to_lines(self.instance.ideal_paths)
            self.fields['overview'].initial = _list_to_lines(self.instance.overview)
            self.fields['curriculum'].initial = _curriculum_to_text(self.instance.curriculum)
            self.fields['reviews'].initial = _reviews_to_text(self.instance.reviews)
        for name in [
            'salary_range', 'career_label', 'career_min', 'career_max',
            'highlight_quote', 'highlight_author', 'starts_with', 'image',
        ]:
            self.fields[name].required = False
        self.fields['featured'].required = False
        self.fields['is_active'].required = False

    def clean_gains(self):
        return _lines_to_list(self.cleaned_data.get('gains'))

    def clean_includes(self):
        return _lines_to_list(self.cleaned_data.get('includes'))

    def clean_learn_modules(self):
        return _lines_to_list(self.cleaned_data.get('learn_modules'))

    def clean_ideal_paths(self):
        return _lines_to_list(self.cleaned_data.get('ideal_paths'))

    def clean_overview(self):
        return _lines_to_list(self.cleaned_data.get('overview'))

    def clean_curriculum(self):
        return _parse_curriculum(self.cleaned_data.get('curriculum'))

    def clean_reviews(self):
        return _parse_reviews(self.cleaned_data.get('reviews'))

    def save(self, commit=True):
        course = super().save(commit=False)
        if not course.slug:
            course.slug = unique_course_slug(course.title, exclude_pk=course.pk)
        if commit:
            course.save()
        return course
