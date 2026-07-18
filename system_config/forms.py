from django import forms
from .models import SystemSettings, Testimonial, Achievement, HighlightSlide
from accounts.models import User, StaffRole, College


class SystemSettingsForm(forms.ModelForm):
    """Form for system settings"""
    class Meta:
        model = SystemSettings
        fields = ['treasurer_whatsapp', 'treasurer_name', 'lipa_namba', 'lipa_namba_name', 
                  'whatsapp_group_link', 'contact_phone', 'contact_email', 'contact_whatsapp']
        widgets = {
            'treasurer_whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'treasurer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lipa_namba': forms.TextInput(attrs={'class': 'form-control'}),
            'lipa_namba_name': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_group_link': forms.URLInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TestimonialForm(forms.ModelForm):
    """Form for testimonials"""
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'avatar_initials', 'content', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar_initials': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AchievementForm(forms.ModelForm):
    """Form for achievements"""
    class Meta:
        model = Achievement
        fields = ['year', 'title', 'image', 'is_active', 'order']
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HighlightSlideForm(forms.ModelForm):
    """Form for highlight slides"""
    class Meta:
        model = HighlightSlide
        fields = ['title', 'description', 'image', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StaffForm(forms.ModelForm):
    """Form for creating/editing staff members"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'staff_role', 'assigned_college', 'is_staff']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_role': forms.Select(attrs={'class': 'form-control'}),
            'assigned_college': forms.Select(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_college'].required = False
        self.fields['staff_role'].required = False
