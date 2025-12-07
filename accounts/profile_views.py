from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """User profile page"""
    try:
        application = request.user.application
    except:
        application = None
    
    context = {
        'application': application,
    }
    return render(request, 'accounts/profile.html', context)


def about_us(request):
    """About IET page"""
    return render(request, 'accounts/about.html')


@login_required
def notifications(request):
    """User notifications page"""
    notifications = request.user.notifications.all()
    
    # Mark all as read when viewing
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'accounts/notifications.html', context)






