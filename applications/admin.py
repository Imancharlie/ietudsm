from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'university', 'course', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'university')
    search_fields = ('first_name', 'last_name', 'email', 'university', 'course')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'nationality')
        }),
        ('Address', {
            'fields': ('address', 'city')
        }),
        ('Academic Information', {
            'fields': ('department', 'course', 'year_of_study', 'date_of_admission')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')




