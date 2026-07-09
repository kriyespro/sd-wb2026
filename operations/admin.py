from django.contrib import admin

from .models import (
    Assessment,
    PerformanceReview,
    ProjectAssignment,
    Team,
    TeamMember,
)


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TeamMemberInline]


@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'can_contact_client', 'assigned_at')
    list_filter = ('role', 'can_contact_client')


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'title', 'score', 'status')
    list_filter = ('status',)


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'rating', 'reviewer', 'created_at')
