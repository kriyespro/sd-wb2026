from clients.models import ClientAccount

from .models import Invoice


def get_client_invoices(account):
    if not account:
        return Invoice.objects.none()
    return Invoice.objects.filter(client_account=account).select_related('project')


def get_all_invoices():
    return Invoice.objects.select_related('client_account', 'project')
