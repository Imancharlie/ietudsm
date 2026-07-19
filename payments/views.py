from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .models import Payment
from applications.models import Application, ApplicationStatus
from services import send_sms

@user_passes_test(lambda u: u.is_staff)
def confirm_payment(request, pk):
    """Staff confirms payment for an application"""
    payment = get_object_or_404(Payment, pk=pk)
    
    if payment.is_confirmed:
        messages.warning(request, 'Payment already confirmed.')
        return redirect('applications:staff_detail', pk=payment.application.pk)
    
    if request.method == 'POST':
        payment.is_confirmed = True
        payment.confirmed_by = request.user
        payment.confirmed_at = timezone.now()
        payment.save()
        
        # Update application status
        application = payment.application
        application.status = ApplicationStatus.PAYMENT_CONFIRMED
        application.save()
        
        # Mark user as approved member
        application.user.is_approved_member = True
        application.user.save()
        
        # Send SMS to user welcoming them to IET UDSM (inactive for now)
        # welcome_message = f"Welcome to the IET UDSM Student Chapter! Your payment has been received and you are now a member of IET. Your journey to becoming That Engineer begins now. Start building your professional CV if you don't have one yet, maintain an active LinkedIn profile, and take every opportunity to participate in IET workshops, projects, competitions, networking events, and leadership initiatives. Every experience shapes the engineer you'll become. Welcome to the family! Join our WhatsApp group: {settings.WHATSAPP_GROUP_LINK} #BEingThatEngineer"
        # send_sms(application.phone_number, welcome_message)
        
        messages.success(request, f'Payment confirmed for {application.full_name}. User is now an approved member.')
        return redirect('applications:staff_detail', pk=application.pk)
    
    context = {
        'payment': payment,
        'application': payment.application,
    }
    return render(request, 'payments/confirm.html', context)


@user_passes_test(lambda u: u.is_staff)
def reject_payment(request, pk):
    """Staff rejects payment for an application"""
    payment = get_object_or_404(Payment, pk=pk)
    
    if payment.is_confirmed:
        messages.warning(request, 'Cannot reject a confirmed payment.')
        return redirect('applications:staff_detail', pk=payment.application.pk)
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        payment.is_rejected = True
        payment.rejection_reason = rejection_reason
        payment.save()
        
        # Update application status back to submitted
        application = payment.application
        application.status = ApplicationStatus.SUBMITTED
        application.save()
        
        messages.warning(request, f'Payment rejected for {application.full_name}. User has been notified.')
        return redirect('applications:staff_detail', pk=application.pk)
    
    context = {
        'payment': payment,
        'application': payment.application,
    }
    return render(request, 'payments/reject.html', context)




