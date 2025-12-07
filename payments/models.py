from django.db import models
from django.conf import settings
import uuid


class Payment(models.Model):
    application = models.OneToOneField('applications.Application', on_delete=models.CASCADE, related_name='payment')
    reference_number = models.CharField(max_length=100, unique=True, editable=False)
    
    # Payment proof from user
    wakala_number = models.CharField(max_length=50, blank=True, null=True, help_text="Control/Wakala number from payment receipt")
    sender_name = models.CharField(max_length=200, blank=True, null=True, help_text="Name of person who made the payment")
    
    # Confirmation status
    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_payments'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    def __str__(self):
        return f"Payment {self.reference_number} - {self.application.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generate unique reference number
            self.reference_number = f"IET-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)




