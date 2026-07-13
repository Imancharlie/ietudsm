from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from .models import Application, ApplicationStatus
from payments.models import Payment
from certificates.models import Certificate


@user_passes_test(lambda u: u.is_staff)
def staff_dashboard(request):
    """Staff dashboard with overview statistics"""
    from accounts.models import StaffRole
    from applications.course_mappings import COURSE_COLLEGE_MAPPING
    
    # Get base queryset
    applications_queryset = Application.objects.all()
    
    # Filter by college for Coordinators
    if request.user.staff_role == StaffRole.COORDINATOR and request.user.assigned_college:
        applications_queryset = applications_queryset.filter(course__in=[
            course for course, college in COURSE_COLLEGE_MAPPING.items()
            if college == request.user.assigned_college
        ])
    
    # Get statistics
    total_applications = applications_queryset.count()
    pending_payments = applications_queryset.filter(status=ApplicationStatus.SUBMITTED).count()
    
    # Count certificates that are ready (completed status)
    ready_certificates = Certificate.objects.filter(
        is_ready=True,
        application__in=applications_queryset
    ).count()
    
    # Count applications in certificate processing (pending certificates)
    pending_certificates = applications_queryset.filter(
        status__in=[ApplicationStatus.CERTIFICATE_PROCESSING]
    ).count()
    
    # Get recent applications (last 10)
    recent_applications = applications_queryset.order_by('-created_at')[:10]
    
    # Get pending payment confirmations
    pending_payment_list = Payment.objects.filter(
        is_confirmed=False,
        is_rejected=False,
        application__in=applications_queryset
    ).select_related('application').order_by('-created_at')[:10]
    
    # Role-specific data
    user_role = request.user.staff_role
    can_confirm_payments = request.user.can_confirm_payments()
    can_manage_certificates = request.user.can_manage_certificates()
    
    context = {
        'total_applications': total_applications,
        'pending_payments': pending_payments,
        'pending_certificates': pending_certificates,
        'ready_certificates': ready_certificates,
        'recent_applications': recent_applications,
        'pending_payment_list': pending_payment_list,
        'user_role': user_role,
        'can_confirm_payments': can_confirm_payments,
        'can_manage_certificates': can_manage_certificates,
        'is_coordinator': request.user.staff_role == StaffRole.COORDINATOR,
        'assigned_college': request.user.assigned_college,
    }
    
    return render(request, 'applications/staff_dashboard.html', context)

