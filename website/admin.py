from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'company', 'service_interest', 'status',
        'source_page', 'assigned_to', 'created_at',
    )
    list_filter = ('status', 'source_page', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'message', 'handoff_notes')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('assigned_to', 'converted_client')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        ('Contact', {
            'fields': ('name', 'email', 'phone', 'company', 'service_interest', 'message', 'source_page'),
        }),
        ('Pipeline', {
            'fields': ('status', 'assigned_to', 'handoff_notes', 'converted_client'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
