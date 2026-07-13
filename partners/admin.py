from django.contrib import admin

from .models import (
    Commission,
    DgcApplication,
    PartnerLead,
    PartnerOrder,
    PartnerProfile,
    PayoutRequest,
    ResellerOffer,
)


@admin.register(DgcApplication)
class DgcApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'phone', 'city', 'why')
    readonly_fields = ('created_at', 'updated_at', 'partner_user', 'temp_password')


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'upi_id', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('code', 'user__username', 'user__email', 'upi_id')


@admin.register(ResellerOffer)
class ResellerOfferAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'market_price_min', 'market_price_max',
        'billing_note', 'commission_percent', 'is_active', 'sort_order',
    )
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(PartnerOrder)
class PartnerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner', 'offer', 'quantity', 'total', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('partner__code', 'offer__title')


@admin.register(PartnerLead)
class PartnerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'phone', 'company', 'status', 'deal_value', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email', 'company', 'partner__code')


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('partner', 'amount', 'source', 'status', 'created_at')
    list_filter = ('source', 'status')
    search_fields = ('partner__code', 'note')


@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    list_display = ('partner', 'amount', 'period_month', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('partner__code',)
