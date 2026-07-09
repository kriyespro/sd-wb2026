from django.contrib import admin

from .models import (
    Deliverable,
    Meeting,
    Milestone,
    Project,
    Report,
    ReportMetric,
)


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0


class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 0
    fields = ('title', 'approval_status', 'file_url')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_account', 'service_type', 'status', 'progress_percent', 'project_manager')
    list_filter = ('status', 'service_type')
    search_fields = ('name', 'client_account__company_name')
    inlines = [MilestoneInline, DeliverableInline]


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'approval_status', 'approved_by', 'created_at')
    list_filter = ('approval_status',)
    actions = ['approve_deliverables']

    @admin.action(description='Approve selected deliverables (make client-visible)')
    def approve_deliverables(self, request, queryset):
        queryset.update(approval_status=Deliverable.APPROVAL_APPROVED, approved_by=request.user)


class ReportMetricInline(admin.TabularInline):
    model = ReportMetric
    extra = 0


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'period', 'created_at')
    inlines = [ReportMetricInline]


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_account', 'scheduled_at', 'status')
    list_filter = ('status',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status')
    list_filter = ('status',)
