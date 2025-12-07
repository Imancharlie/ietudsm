from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from applications.models import ApplicationStatus
from accounts.models import Notification


@receiver(post_save, sender=Payment)
def update_user_approval_on_payment_confirmation(sender, instance, created, **kwargs):
    """
    Automatically update user's is_approved_member flag when payment is confirmed.
    This ensures consistency even if payment is confirmed through admin panel.
    """
    if instance.is_confirmed and not instance.is_rejected:
        user = instance.application.user
        
        # Update user approval status
        if not user.is_approved_member:
            user.is_approved_member = True
            user.save()
            
            # Create notification for payment confirmation
            Notification.objects.create(
                user=user,
                title='Payment Confirmed!',
                message=f'Your payment of 10,000 TZS has been confirmed. Welcome to IET! You can now access your dashboard.',
                notification_type='payment_confirmed'
            )
        
        # Update application status
        if instance.application.status != ApplicationStatus.PAYMENT_CONFIRMED:
            instance.application.status = ApplicationStatus.PAYMENT_CONFIRMED
            instance.application.save()
    
    # Handle payment rejection
    elif instance.is_rejected and not created:
        user = instance.application.user
        
        # Create notification for payment rejection
        Notification.objects.create(
            user=user,
            title='Payment Rejected',
            message=f'Your payment has been rejected. Reason: {instance.rejection_reason}. Please contact the treasurer for more information.',
            notification_type='payment_rejected'
        )

