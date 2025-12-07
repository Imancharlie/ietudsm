from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, ApplicationStatus
from accounts.models import User, Notification


@receiver(post_save, sender=Application)
def notify_staff_on_new_application(sender, instance, created, **kwargs):
    """
    Notify all staff members when a new application is submitted
    """
    # Only notify when application status changes to SUBMITTED
    if instance.status == ApplicationStatus.SUBMITTED:
        # Check if we've already notified for this application
        # (to avoid duplicate notifications on updates)
        existing_notifications = Notification.objects.filter(
            notification_type='general',
            message__contains=f'{instance.full_name} has submitted'
        )
        
        if not existing_notifications.exists():
            # Get all staff members
            staff_users = User.objects.filter(is_staff=True)
            
            # Create notification for each staff member
            for staff_user in staff_users:
                Notification.objects.create(
                    user=staff_user,
                    title='New Application Submitted',
                    message=f'{instance.full_name} has submitted a new membership application. Reference: {instance.payment.reference_number if hasattr(instance, "payment") else "N/A"}',
                    notification_type='general'
                )

