from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .models import Application, ApplicationStatus
from .forms import ApplicationForm
from payments.models import Payment
from payments.forms import PaymentProofForm


@login_required
def create_application(request):
    """Create or update application form"""
    # Try to get existing application, but don't create if it doesn't exist
    try:
        application = Application.objects.get(user=request.user)
    except Application.DoesNotExist:
        application = None
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application, user=request.user)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            
            # Set department from course mapping
            from applications.course_mappings import get_department_from_course
            app.department = get_department_from_course(app.course)
            
            # Always save as draft first
            app.status = ApplicationStatus.DRAFT
            
            # Save the application first
            app.save()
            
            # Now create payment reference after application is saved
            payment, payment_created = Payment.objects.get_or_create(application=app)
            
            if 'submit_application' in request.POST:
                # Redirect to preview page for payment
                messages.info(request, 'Please review your application and complete payment before final submission.')
                return redirect('applications:preview')
            else:
                messages.info(request, 'Application saved as draft.')
                return redirect('applications:create')
    else:
        form = ApplicationForm(instance=application, user=request.user)
    
    # Get or create payment reference only if application exists
    payment = None
    if application:
        payment, _ = Payment.objects.get_or_create(application=application)
    
    context = {
        'form': form,
        'application': application,
        'payment': payment,
        'registration_fee': settings.REGISTRATION_FEE,
    }
    return render(request, 'applications/create.html', context)


@login_required
def application_status(request):
    """View application status"""
    # If user is approved member, redirect to dashboard
    if request.user.is_approved_member:
        messages.success(request, 'Your payment has been confirmed! Welcome to IET.')
        return redirect('dashboard:index')
    
    try:
        application = request.user.application
        payment = Payment.objects.get(application=application)
    except Application.DoesNotExist:
        messages.info(request, 'Please complete your application form first.')
        return redirect('applications:create')
    except Payment.DoesNotExist:
        payment = None
    
    # Coordinator contact based on department
    # This is a simple mapping - you can make it more sophisticated
    coordinator_contacts = {
        'Mechanical and Industrial Engineering Department': '+255123456789',  # Replace with actual
        'Electrical Engineering Department': '+255123456789',  # Replace with actual
        'Civil Engineering Department': '+255123456789',  # Replace with actual
        'Chemical Engineering Department': '+255123456789',  # Replace with actual
        'Transportation and Geotechnical Engineering Department': '+255123456789',  # Replace with actual
        'Departments of Structural and Construction Engineering': '+255123456789',  # Replace with actual
        'Metallurgy and Mineral Processing Department': '+255123456789',  # Replace with actual
        'Geology and Mining Department': '+255123456789',  # Replace with actual
    }
    
    coordinator_whatsapp = coordinator_contacts.get(
        application.department if application else None,
        settings.TREASURER_WHATSAPP  # Default to treasurer if no match
    )
    
    context = {
        'application': application,
        'payment': payment,
        'registration_fee': settings.REGISTRATION_FEE,
        'treasurer_whatsapp': settings.TREASURER_WHATSAPP,
        'coordinator_whatsapp': coordinator_whatsapp,
    }
    return render(request, 'applications/status.html', context)


@login_required
def application_preview(request):
    """Preview application before final submission with payment"""
    try:
        application = Application.objects.get(user=request.user)
    except Application.DoesNotExist:
        messages.error(request, 'Please complete your application form first.')
        return redirect('applications:create')
    
    # Get or create payment
    payment, _ = Payment.objects.get_or_create(application=application)
    
    # Handle payment proof submission
    if request.method == 'POST':
        if 'submit_proof' in request.POST:
            proof_form = PaymentProofForm(request.POST, instance=payment)
            if proof_form.is_valid():
                # Reset rejection status on resubmission
                payment_obj = proof_form.save(commit=False)
                payment_obj.is_rejected = False
                payment_obj.rejection_reason = None
                payment_obj.save()
                
                # Submit application
                application.status = ApplicationStatus.SUBMITTED
                application.save()
                request.user.has_completed_application = True
                request.user.save()
                
                # Send SMS to treasurer about new application
                from services import send_sms
                treasurer_phone = settings.TREASURER_PHONE
                
                sms_message = f"New IET Registration Application Submitted!\nName: {application.full_name}\n Sender Name on the transaction: {payment_obj.sender_name}\n Course: {application.course}\nPhone: {application.phone_number}\n\nPlease review the application and confirm the payment if received."
                
                # Send to treasurer's number from settings
                send_sms(treasurer_phone, sms_message)
                # Also send to the specific number 0792267622
                send_sms("0792267622", sms_message)
                
                # Create welcome notification for new member
                from accounts.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title="Welcome to IET UDSM!",
                    message="Welcome to the IET UDSM Student Chapter! Your journey to becoming 'That Engineer' starts now. Remember to create a professional CV early, build your LinkedIn profile, and actively participate in IET activities. Every workshop, project, and leadership opportunity brings you closer to engineering excellence.",
                    notification_type='general'
                )
                
                messages.success(request, 'Application submitted successfully! Staff will review your payment.')
                return redirect('applications:status')
        elif 'edit_application' in request.POST:
            return redirect('applications:create')
    
    proof_form = PaymentProofForm(instance=payment)
    
    context = {
        'application': application,
        'payment': payment,
        'proof_form': proof_form,
        'registration_fee': settings.REGISTRATION_FEE,
        'treasurer_whatsapp': settings.TREASURER_WHATSAPP,
        'lipa_namba': settings.LIPA_NAMBA,
        'lipa_namba_name': settings.LIPA_NAMBA_NAME,
    }
    return render(request, 'applications/preview.html', context)


@user_passes_test(lambda u: u.is_staff)
def staff_application_list(request):
    """Staff view of all applications with search functionality"""
    from accounts.models import StaffRole
    from applications.course_mappings import COURSE_COLLEGE_MAPPING
    status_filter = request.GET.get('status', '')
    show_all = request.GET.get('show_all', '') == 'true'
    search_query = request.GET.get('search', '')

    applications = Application.objects.all()

    # Filter by college for Coordinators (unless show_all is true)
    if request.user.staff_role == StaffRole.COORDINATOR and request.user.assigned_college and not show_all:
        applications = applications.filter(course__in=[
            course for course, college in COURSE_COLLEGE_MAPPING.items()
            if college == request.user.assigned_college
        ])

    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Search functionality
    if search_query:
        applications = applications.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(department__icontains=search_query)
        )

    context = {
        'applications': applications,
        'status_choices': ApplicationStatus.choices,
        'current_filter': status_filter,
        'is_coordinator': request.user.staff_role == StaffRole.COORDINATOR,
        'assigned_college': request.user.assigned_college,
        'showing_all': show_all,
        'search_query': search_query,
    }
    return render(request, 'applications/staff_list.html', context)


@user_passes_test(lambda u: u.is_staff)
def staff_application_detail(request, pk):
    """Staff view of application details"""
    application = get_object_or_404(Application, pk=pk)
    payment = Payment.objects.filter(application=application).first()
    
    context = {
        'application': application,
        'payment': payment,
    }
    return render(request, 'applications/staff_detail.html', context)




