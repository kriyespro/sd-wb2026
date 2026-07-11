from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import timesince
from django.urls import reverse
from django.utils import timezone
from jinja2 import Environment


def timeago(value):
    """Compact relative time for dense ops feeds: 5m, 2h, 3d, 1w."""
    if not value:
        return ''
    now = timezone.now()
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())
    seconds = int((now - value).total_seconds())
    if seconds < 0:
        seconds = 0
    if seconds < 60:
        return 'now'
    minutes = seconds // 60
    if minutes < 60:
        return f'{minutes}m'
    hours = minutes // 60
    if hours < 24:
        return f'{hours}h'
    days = hours // 24
    if days < 7:
        return f'{days}d'
    if days < 30:
        weeks = days // 7
        return f'{weeks}w'
    return value.strftime('%d %b')


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'timesince': timesince,
        'timeago': timeago,
    })
    return env
