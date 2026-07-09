from django.contrib import admin

from .models import ClientAccount, Goal, SupportMessage, SupportTicket


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'account_manager', 'created_at')
    search_fields = ('company_name', 'user__username', 'user__email')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_account', 'progress_percent', 'status')
    list_filter = ('status',)


class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'client_account', 'status', 'updated_at')
    list_filter = ('status',)
    inlines = [SupportMessageInline]
