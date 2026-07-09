from django.conf import settings
from django.core.mail import send_mail

from .models import Lead


def create_lead(form, source_page=''):
    lead = form.save(commit=False)
    lead.source_page = source_page
    lead.save()
    notify_lead_created(lead)
    return lead


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
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=True,
    )
