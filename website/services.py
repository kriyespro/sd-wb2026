import logging
import threading

from django.conf import settings
from django.core.mail import send_mail

from .models import JobApplication, Lead

logger = logging.getLogger(__name__)


def create_lead(form, source_page=''):
    lead = form.save(commit=False)
    lead.source_page = source_page
    lead.save()
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
