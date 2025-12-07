from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class StaffRole(models.TextChoices):
    """Staff roles for permission management"""
    GENERAL_SECRETARY = 'general_secretary', 'General Secretary'
    TREASURER = 'treasurer', 'Treasurer'
    CHAIRPERSON = 'chairperson', 'Chairperson'
    VICE_CHAIRPERSON = 'vice_chairperson', 'Vice Chairperson'
    COORDINATOR = 'coordinator', 'Coordinator'
    ADMIN = 'admin', 'Administrator'


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    is_approved_member = models.BooleanField(default=False, help_text="True if payment is confirmed")
    has_completed_application = models.BooleanField(default=False, help_text="True if application form is submitted")
    staff_role = models.CharField(
        max_length=50,
        choices=StaffRole.choices,
        blank=True,
        null=True,
        help_text="Role for staff members"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
    
    def unread_notifications_count(self):
        """Get count of unread notifications"""
        return self.notifications.filter(is_read=False).count()
    
    def has_role(self, role):
        """Check if user has a specific staff role"""
        return self.is_staff and self.staff_role == role
    
    def can_confirm_payments(self):
        """Check if user can confirm payments (Treasurer or Admin)"""
        return self.is_staff and self.staff_role in [StaffRole.TREASURER, StaffRole.ADMIN, StaffRole.CHAIRPERSON]
    
    def can_manage_certificates(self):
        """Check if user can manage certificates"""
        return self.is_staff and self.staff_role in [StaffRole.GENERAL_SECRETARY, StaffRole.ADMIN, StaffRole.CHAIRPERSON]
    
    def can_post_announcements(self):
        """Check if user can post announcements"""
        return self.is_staff  # All staff can post announcements


class Notification(models.Model):
    """User notifications for payment confirmations, rejections, etc."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('payment_confirmed', 'Payment Confirmed'),
        ('payment_rejected', 'Payment Rejected'),
        ('certificate_ready', 'Certificate Ready'),
        ('general', 'General'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"




