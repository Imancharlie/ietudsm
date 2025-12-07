from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'staff_role', 'is_approved_member', 'has_completed_application', 'date_joined')
    list_filter = ('is_staff', 'staff_role', 'is_approved_member', 'has_completed_application')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('IET Membership', {
            'fields': ('is_approved_member', 'has_completed_application')
        }),
        ('Staff Role', {
            'fields': ('staff_role',),
            'description': 'Assign a role to staff members for permission management'
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at',)




