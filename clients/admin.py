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
    list_display = ('subject', 'client_account', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'client_account__company_name', 'messages__body')
    inlines = [SupportMessageInline]
    date_hierarchy = 'created_at'


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'body_preview', 'created_at')
    search_fields = ('body', 'ticket__subject', 'sender__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    @admin.display(description='Message')
    def body_preview(self, obj):
        return obj.body[:80] + ('…' if len(obj.body) > 80 else '')
