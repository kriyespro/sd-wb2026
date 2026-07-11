from django.contrib import admin

from .models import JobApplication, Lead


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


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone', 'role', 'application_type', 'status', 'created_at',
    )
    list_filter = ('status', 'application_type', 'role', 'created_at')
    search_fields = ('name', 'email', 'phone', 'role', 'cover_letter', 'experience')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        ('Applicant', {
            'fields': (
                'name', 'email', 'phone', 'role', 'application_type',
                'experience', 'portfolio_url', 'linkedin_url', 'cover_letter',
            ),
        }),
        ('Review', {
            'fields': ('status', 'created_at'),
        }),
    )
