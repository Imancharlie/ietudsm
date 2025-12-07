from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Certificate
from accounts.models import Notification


@receiver(post_save, sender=Certificate)
def notify_user_certificate_ready(sender, instance, created, **kwargs):
    """
    Notify user when their certificate is marked as ready
    """
    # Only notify when certificate is marked as ready
    if instance.is_ready and instance.ready_at:
        user = instance.application.user
        
        # Check if we've already notified for this certificate
        existing_notification = Notification.objects.filter(
            user=user,
            notification_type='certificate_ready',
            message__contains='certificate is ready'
        ).exists()
        
        if not existing_notification:
            # Create notification without certificate number
            Notification.objects.create(
                user=user,
                title='Certificate Ready!',
                message='Your IET membership certificate is ready for collection. Please come to Room A11 to collect your certificate.',
                notification_type='certificate_ready'
            )

