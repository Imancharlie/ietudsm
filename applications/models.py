from django.db import models
from django.conf import settings
import uuid


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted – Awaiting Payment Confirmation'
    PAYMENT_CONFIRMED = 'payment_confirmed', 'Payment Confirmed'
    UNDER_REVIEW = 'under_review', 'Under Review'
    CERTIFICATE_PROCESSING = 'certificate_processing', 'Certificate Processing'
    COMPLETED = 'completed', 'Completed (Approved)'


class Application(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='application')
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20, default='')
    
    # Nationality
    nationality = models.CharField(max_length=100, default='Tanzanian')
    
    # Address
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # Made optional for migration
    
    # University & Department
    university = models.CharField(max_length=200, default='University of Dar es Salaam', editable=False)
    department = models.CharField(max_length=200)
    
    # Course & Year
    course = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=50)
    date_of_admission = models.IntegerField(help_text='Year of admission (e.g., 2023)', default=2024)
    
    # Age & Date of Birth
    date_of_birth = models.DateField()
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    @property
    def year_of_graduation(self):
        """Calculate expected year of graduation based on admission year + 4 years"""
        # Use admission year + 4 for accurate graduation calculation
        return self.date_of_admission + 4
    
    @property
    def admission_date_formatted(self):
        """Format admission date as Nov/YYYY"""
        return f"Nov/{self.date_of_admission}"
    
    # Application Status
    status = models.CharField(
        max_length=50,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.DRAFT
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Application"
        verbose_name_plural = "Applications"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def college(self):
        """Get college from course using mapping"""
        from applications.course_mappings import get_college_from_course
        return get_college_from_course(self.course)




