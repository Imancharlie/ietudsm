from django.db import models
from django.conf import settings


class Certificate(models.Model):
    application = models.OneToOneField('applications.Application', on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_ready = models.BooleanField(default=False)
    ready_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
    
    def __str__(self):
        return f"Certificate for {self.application.full_name} - {'Ready' if self.is_ready else 'Not Ready'}"




