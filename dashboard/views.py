from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from applications.models import Application
from certificates.models import Certificate
from announcements.models import Announcement


@login_required
def index(request):
    """User dashboard - only accessible after payment confirmation"""
    if not request.user.is_approved_member:
        return redirect('applications:status')
    
    try:
        application = request.user.application
        certificate = Certificate.objects.filter(application=application).first()
    except Application.DoesNotExist:
        application = None
        certificate = None
    
    # Get recent announcements
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'application': application,
        'certificate': certificate,
        'announcements': announcements,
        'whatsapp_link': settings.WHATSAPP_GROUP_LINK,
    }
    return render(request, 'dashboard/index.html', context)

