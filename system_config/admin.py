from django.contrib import admin
from .models import SystemSettings, Testimonial, Achievement, HighlightSlide


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """Admin interface for system settings"""
    list_display = ['treasurer_name', 'contact_phone', 'contact_email', 'updated_at']
    fieldsets = (
        ('Treasurer Information', {
            'fields': ('treasurer_whatsapp', 'treasurer_name')
        }),
        ('Payment Information', {
            'fields': ('lipa_namba', 'lipa_namba_name')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'contact_whatsapp')
        }),
        ('Social Links', {
            'fields': ('whatsapp_group_link',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for testimonials"""
    list_display = ['name', 'role', 'is_active', 'order', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'content']
    list_editable = ['is_active', 'order']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin interface for achievements"""
    list_display = ['year', 'title', 'is_active', 'order', 'updated_at']
    list_filter = ['is_active', 'year']
    search_fields = ['title', 'year']
    list_editable = ['is_active', 'order']


@admin.register(HighlightSlide)
class HighlightSlideAdmin(admin.ModelAdmin):
    """Admin interface for highlight slides"""
    list_display = ['title', 'is_active', 'order', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
