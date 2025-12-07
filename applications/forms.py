from django import forms
from .models import Application, ApplicationStatus
from .course_mappings import COURSE_DEPARTMENT_MAPPING, YEAR_OF_STUDY_CHOICES, get_department_from_course
from datetime import date


class ApplicationForm(forms.ModelForm):
    course = forms.ChoiceField(
        choices=[('', 'Select your course')] + [(course, course) for course in sorted(COURSE_DEPARTMENT_MAPPING.keys())],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year_of_study = forms.ChoiceField(
        choices=[('', 'Select year of study')] + YEAR_OF_STUDY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Application
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
            'nationality',
            'address', 'city',
            'course', 'year_of_study', 'date_of_admission',
            'date_of_birth'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle name (optional)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +255 712 345 678'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Tanzanian'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'date_of_admission': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2023', 'min': '2000', 'max': '2030'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_date_of_birth'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill email from user account
        if user and not self.instance.pk:
            self.fields['email'].initial = user.email
        
        # Set nationality default
        if not self.instance.pk:
            self.fields['nationality'].initial = 'Tanzanian'
    
    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        
        # Auto-set department based on course
        if course:
            cleaned_data['department'] = get_department_from_course(course)
        
        return cleaned_data




