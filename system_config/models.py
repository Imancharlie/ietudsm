from django.db import models


class SystemSettings(models.Model):
    """System-wide configuration settings"""
    treasurer_whatsapp = models.CharField(max_length=20, default="+255763167686", help_text="Treasurer WhatsApp number")
    treasurer_name = models.CharField(max_length=100, default="IET Treasurer", help_text="Treasurer name")
    lipa_namba = models.CharField(max_length=20, default="06989001197", help_text="LIPA NAMBA number")
    lipa_namba_name = models.CharField(max_length=100, default="IET UDSM", help_text="LIPA NAMBA account name")
    whatsapp_group_link = models.URLField(default="https://chat.whatsapp.com/HWTg4c6JKcUJi69RCZHaX7", help_text="WhatsApp group link")
    contact_phone = models.CharField(max_length=20, default="0614021404", help_text="Main contact phone")
    contact_email = models.EmailField(default="udsmiet@gmail.com", help_text="Main contact email")
    contact_whatsapp = models.CharField(max_length=20, default="+255763167686", help_text="Main contact WhatsApp")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "System Settings"
        verbose_name_plural = "System Settings"
    
    def __str__(self):
        return "System Configuration"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SystemSettings.objects.exists():
            raise ValueError("Only one SystemSettings instance can exist")
        return super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Testimonials for landing page"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    avatar_initials = models.CharField(max_length=3, help_text="2-3 letters for avatar")
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class Achievement(models.Model):
    """Achievements for landing page slideshow"""
    year = models.CharField(max_length=10, help_text="Year of achievement")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='achievements/')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
    
    def __str__(self):
        return f"{self.year} - {self.title}"


class HighlightSlide(models.Model):
    """Highlight slideshow images for landing page"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='highlights/')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Highlight Slide"
        verbose_name_plural = "Highlight Slides"
    
    def __str__(self):
        return self.title
