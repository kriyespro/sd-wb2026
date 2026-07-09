from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'company', 'service_interest', 'status',
        'assigned_to', 'source_page', 'created_at',
    )
    list_filter = ('status', 'source_page', 'created_at')
    search_fields = ('name', 'email', 'company', 'message', 'handoff_notes')
    readonly_fields = ('created_at', 'updated_at', 'converted_client')
    raw_id_fields = ('assigned_to', 'converted_client')
