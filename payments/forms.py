from django import forms
from .models import Payment


class PaymentProofForm(forms.ModelForm):
    """Form for users to submit payment proof"""
    
    class Meta:
        model = Payment
        fields = ['sender_name', 'wakala_number']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter name or phone number from receipt',
                'required': True
            }),
            'wakala_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter if available',
                'required': False
            }),
        }
        labels = {
            'sender_name': 'Sender Name or Phone Number',
            'wakala_number': 'Control/Wakala Number (Optional)',
        }
        help_texts = {
            'sender_name': 'Jina au namba ya simu iliyotumia malipo',
            'wakala_number': '',
        }




