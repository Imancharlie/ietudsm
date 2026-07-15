from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


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


@login_required
def settings(request):
    """User settings page with password change"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('accounts:settings')
        
        # Validate new password
        if len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
            return redirect('accounts:settings')
        
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('accounts:settings')
        
        if current_password == new_password:
            messages.error(request, 'New password must be different from current password.')
            return redirect('accounts:settings')
        
        # Update password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Password updated successfully!')
        return redirect('accounts:settings')
    
    return render(request, 'accounts/settings.html')






