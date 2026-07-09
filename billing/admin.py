from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client_account', 'title', 'amount', 'status', 'due_date', 'issued_at')
    list_filter = ('status', 'issued_at')
    search_fields = ('invoice_number', 'title', 'client_account__company_name')
