from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'application', 'wakala_number', 'is_confirmed', 'is_rejected', 'confirmed_by', 'confirmed_at', 'created_at')
    list_filter = ('is_confirmed', 'is_rejected', 'created_at', 'confirmed_at')
    search_fields = ('reference_number', 'wakala_number', 'sender_name', 'application__first_name', 'application__last_name')
    readonly_fields = ('reference_number', 'created_at', 'updated_at')
    fieldsets = (
        ('Payment Information', {
            'fields': ('application', 'reference_number', 'is_confirmed', 'is_rejected')
        }),
        ('Payment Proof from User', {
            'fields': ('wakala_number', 'sender_name'),
            'description': 'Payment proof submitted by the applicant'
        }),
        ('Confirmation Details', {
            'fields': ('confirmed_by', 'confirmed_at')
        }),
        ('Rejection Details', {
            'fields': ('rejection_reason',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )




