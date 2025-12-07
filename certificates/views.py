from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Certificate
from applications.models import Application, ApplicationStatus


@user_passes_test(lambda u: u.is_staff)
def mark_certificate_ready(request, pk):
    """Staff marks certificate as ready"""
    application = get_object_or_404(Application, pk=pk)
    certificate, created = Certificate.objects.get_or_create(application=application)
    
    if request.method == 'POST':
        certificate.is_ready = True
        certificate.ready_at = timezone.now()
        
        # Generate certificate number if not exists
        if not certificate.certificate_number:
            certificate.certificate_number = f"IET-CERT-{application.id:06d}"
        
        certificate.save()
        
        # Update application status
        application.status = ApplicationStatus.COMPLETED
        application.save()
        
        messages.success(request, f'Certificate marked as ready for {application.full_name}.')
        return redirect('applications:staff_detail', pk=application.pk)
    
    context = {
        'certificate': certificate,
        'application': application,
    }
    return render(request, 'certificates/mark_ready.html', context)


@user_passes_test(lambda u: u.is_staff)
def update_status_to_processing(request, pk):
    """Staff updates status to Certificate Processing"""
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        application.status = ApplicationStatus.CERTIFICATE_PROCESSING
        application.save()
        messages.success(request, f'Status updated to Certificate Processing for {application.full_name}.')
        return redirect('applications:staff_detail', pk=application.pk)
    
    return redirect('applications:staff_detail', pk=application.pk)




