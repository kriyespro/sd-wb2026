import logging
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import JobApplication, Lead, LeadFollowUp

logger = logging.getLogger(__name__)

DEFAULT_FOLLOWUPS = [
    ('called', 'Call / connect attempted'),
    ('message_sent', 'WhatsApp or email sent'),
    ('need_confirmed', 'Client need confirmed'),
    ('quote_shared', 'Quote / package shared'),
    ('followup_set', 'Next follow-up scheduled'),
]


def ensure_lead_followups(lead):
    existing = set(lead.followups.values_list('key', flat=True))
    to_create = [
        LeadFollowUp(lead=lead, key=key, label=label, sort_order=i)
        for i, (key, label) in enumerate(DEFAULT_FOLLOWUPS)
        if key not in existing
    ]
    if to_create:
        LeadFollowUp.objects.bulk_create(to_create)
    return lead.followups.all()


def ensure_lead_followups_bulk(leads):
    """Same as ensure_lead_followups but for many leads in 2 queries total
    instead of ~2 queries per lead — use whenever iterating a lead list."""
    leads = list(leads)
    if not leads:
        return
    existing = set(
        LeadFollowUp.objects.filter(lead__in=leads).values_list('lead_id', 'key'),
    )
    to_create = [
        LeadFollowUp(lead=lead, key=key, label=label, sort_order=i)
        for lead in leads
        for i, (key, label) in enumerate(DEFAULT_FOLLOWUPS)
        if (lead.pk, key) not in existing
    ]
    if to_create:
        LeadFollowUp.objects.bulk_create(to_create)


def toggle_lead_followup(followup, actor, is_done=None):
    followup.is_done = (not followup.is_done) if is_done is None else bool(is_done)
    if followup.is_done:
        followup.done_at = timezone.now()
        followup.done_by = actor
    else:
        followup.done_at = None
        followup.done_by = None
    followup.save(update_fields=['is_done', 'done_at', 'done_by'])
    return followup


def create_lead(form, source_page=''):
    lead = form.save(commit=False)
    lead.source_page = source_page
    lead.save()
    ensure_lead_followups(lead)
    notify_lead_created(lead)
    return lead


def create_job_application(form):
    application = form.save()
    notify_job_application_created(application)
    return application


def _send_lead_email(subject, body, from_email, recipient):
    try:
        send_mail(subject, body, from_email, [recipient], fail_silently=False)
    except Exception:
        logger.exception('Lead notification email failed for %s', recipient)


def notify_lead_created(lead):
    subject = f'New lead: {lead.name} — {lead.service_interest or "General inquiry"}'
    body = (
        f'Name: {lead.name}\n'
        f'Email: {lead.email}\n'
        f'Phone: {lead.phone or "—"}\n'
        f'Company: {lead.company or "—"}\n'
        f'Service: {lead.service_interest or "—"}\n'
        f'Source: {lead.source_page or "—"}\n'
        f'Message:\n{lead.message or "—"}\n'
    )
    recipient = getattr(settings, 'LEAD_NOTIFICATION_EMAIL', None)
    if not recipient:
        return
    threading.Thread(
        target=_send_lead_email,
        args=(subject, body, settings.DEFAULT_FROM_EMAIL, recipient),
        daemon=True,
    ).start()


def notify_job_application_created(application: JobApplication):
    subject = f'Job application: {application.name} — {application.role}'
    body = (
        f'Name: {application.name}\n'
        f'Email: {application.email}\n'
        f'Phone: {application.phone}\n'
        f'Role: {application.role}\n'
        f'Type: {application.get_application_type_display()}\n'
        f'Experience: {application.experience or "—"}\n'
        f'Portfolio: {application.portfolio_url or "—"}\n'
        f'LinkedIn: {application.linkedin_url or "—"}\n'
        f'Cover letter:\n{application.cover_letter}\n'
    )
    recipient = getattr(settings, 'LEAD_NOTIFICATION_EMAIL', None)
    if not recipient:
        return
    threading.Thread(
        target=_send_lead_email,
        args=(subject, body, settings.DEFAULT_FROM_EMAIL, recipient),
        daemon=True,
    ).start()
