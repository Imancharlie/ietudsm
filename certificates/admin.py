from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'application', 'is_ready', 'ready_at', 'created_at')
    list_filter = ('is_ready', 'created_at', 'ready_at')
    search_fields = ('certificate_number', 'application__first_name', 'application__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Certificate Information', {
            'fields': ('application', 'certificate_number', 'is_ready', 'ready_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )




