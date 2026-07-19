from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import SystemSettings, Testimonial, Achievement, HighlightSlide
from .forms import SystemSettingsForm, TestimonialForm, AchievementForm, HighlightSlideForm, StaffForm
from accounts.models import User as CustomUser, StaffRole


def is_admin(user):
    """Check if user is admin (superuser or chairperson)"""
    return user.is_superuser or (user.is_staff and user.staff_role == StaffRole.CHAIRPERSON)


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard"""
    from applications.models import Application
    from accounts.models import Notification
    
    # Get statistics
    total_users = CustomUser.objects.count()
    total_applications = Application.objects.count()
    total_staff = CustomUser.objects.filter(is_staff=True).count()
    total_testimonials = Testimonial.objects.filter(is_active=True).count()
    
    # Get recent activity
    recent_applications = Application.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_applications': total_applications,
        'total_staff': total_staff,
        'total_testimonials': total_testimonials,
        'recent_applications': recent_applications,
    }
    return render(request, 'system_config/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def system_settings(request):
    """Manage system settings"""
    settings_obj = SystemSettings.objects.first()
    
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'System settings updated successfully!')
            return redirect('system_config:settings')
    else:
        form = SystemSettingsForm(instance=settings_obj)
    
    context = {
        'form': form,
        'settings': settings_obj,
    }
    return render(request, 'system_config/settings.html', context)


@login_required
@user_passes_test(is_admin)
def testimonials_list(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'system_config/testimonials_list.html', context)


@login_required
@user_passes_test(is_admin)
def testimonial_create(request):
    """Create new testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial created successfully!')
            return redirect('system_config:testimonials')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
        'title': 'Create Testimonial',
    }
    return render(request, 'system_config/testimonial_form.html', context)


@login_required
@user_passes_test(is_admin)
def testimonial_edit(request, pk):
    """Edit testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('system_config:testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {
        'form': form,
        'title': 'Edit Testimonial',
        'testimonial': testimonial,
    }
    return render(request, 'system_config/testimonial_form.html', context)


@login_required
@user_passes_test(is_admin)
def testimonial_delete(request, pk):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('system_config:testimonials')


@login_required
@user_passes_test(is_admin)
def achievements_list(request):
    """List all achievements"""
    achievements = Achievement.objects.all()
    context = {
        'achievements': achievements,
    }
    return render(request, 'system_config/achievements_list.html', context)


@login_required
@user_passes_test(is_admin)
def achievement_create(request):
    """Create new achievement"""
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement created successfully!')
            return redirect('system_config:achievements')
    else:
        form = AchievementForm()
    
    context = {
        'form': form,
        'title': 'Create Achievement',
    }
    return render(request, 'system_config/achievement_form.html', context)


@login_required
@user_passes_test(is_admin)
def achievement_edit(request, pk):
    """Edit achievement"""
    achievement = get_object_or_404(Achievement, pk=pk)
    
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES, instance=achievement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement updated successfully!')
            return redirect('system_config:achievements')
    else:
        form = AchievementForm(instance=achievement)
    
    context = {
        'form': form,
        'title': 'Edit Achievement',
        'achievement': achievement,
    }
    return render(request, 'system_config/achievement_form.html', context)


@login_required
@user_passes_test(is_admin)
def achievement_delete(request, pk):
    """Delete achievement"""
    achievement = get_object_or_404(Achievement, pk=pk)
    achievement.delete()
    messages.success(request, 'Achievement deleted successfully!')
    return redirect('system_config:achievements')


@login_required
@user_passes_test(is_admin)
def highlights_list(request):
    """List all highlight slides"""
    highlights = HighlightSlide.objects.all()
    context = {
        'highlights': highlights,
    }
    return render(request, 'system_config/highlights_list.html', context)


@login_required
@user_passes_test(is_admin)
def highlight_create(request):
    """Create new highlight slide"""
    if request.method == 'POST':
        form = HighlightSlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Highlight slide created successfully!')
            return redirect('system_config:highlights')
    else:
        form = HighlightSlideForm()
    
    context = {
        'form': form,
        'title': 'Create Highlight Slide',
    }
    return render(request, 'system_config/highlight_form.html', context)


@login_required
@user_passes_test(is_admin)
def highlight_edit(request, pk):
    """Edit highlight slide"""
    highlight = get_object_or_404(HighlightSlide, pk=pk)
    
    if request.method == 'POST':
        form = HighlightSlideForm(request.POST, request.FILES, instance=highlight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Highlight slide updated successfully!')
            return redirect('system_config:highlights')
    else:
        form = HighlightSlideForm(instance=highlight)
    
    context = {
        'form': form,
        'title': 'Edit Highlight Slide',
        'highlight': highlight,
    }
    return render(request, 'system_config/highlight_form.html', context)


@login_required
@user_passes_test(is_admin)
def highlight_delete(request, pk):
    """Delete highlight slide"""
    highlight = get_object_or_404(HighlightSlide, pk=pk)
    highlight.delete()
    messages.success(request, 'Highlight slide deleted successfully!')
    return redirect('system_config:highlights')


@login_required
@user_passes_test(is_admin)
def staff_list(request):
    """List all staff members"""
    staff_members = CustomUser.objects.filter(is_staff=True)
    context = {
        'staff_members': staff_members,
    }
    return render(request, 'system_config/staff_list.html', context)


@login_required
@user_passes_test(is_admin)
def staff_create(request):
    """Create new staff member"""
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set default password
            user.set_password('iet2024')
            user.save()
            messages.success(request, f'Staff member created! Default password: iet2024')
            return redirect('system_config:staff')
    else:
        form = StaffForm()
    
    context = {
        'form': form,
        'title': 'Create Staff Member',
    }
    return render(request, 'system_config/staff_form.html', context)


@login_required
@user_passes_test(is_admin)
def staff_edit(request, pk):
    """Edit staff member"""
    staff = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member updated successfully!')
            return redirect('system_config:staff')
    else:
        form = StaffForm(instance=staff)
    
    context = {
        'form': form,
        'title': 'Edit Staff Member',
        'staff': staff,
    }
    return render(request, 'system_config/staff_form.html', context)


@login_required
@user_passes_test(is_admin)
def staff_delete(request, pk):
    """Delete staff member"""
    staff = get_object_or_404(CustomUser, pk=pk)
    if staff.email == request.user.email:
        messages.error(request, 'You cannot delete yourself!')
        return redirect('system_config:staff')
    
    staff.delete()
    messages.success(request, 'Staff member deleted successfully!')
    return redirect('system_config:staff')
