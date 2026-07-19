from django.shortcuts import render
from system_config.models import SystemSettings, Testimonial, Achievement, HighlightSlide


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)


def custom_403(request, exception):
    """Custom 403 error handler"""
    return render(request, '403.html', status=403)


def landing_page(request):
    """Landing page view with dynamic content from backend"""
    # Get system settings
    settings = SystemSettings.objects.first()
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    
    # Get active achievements
    achievements = Achievement.objects.filter(is_active=True).order_by('order')
    
    # Get active highlight slides
    highlights = HighlightSlide.objects.filter(is_active=True).order_by('order')
    
    context = {
        'settings': settings,
        'testimonials': testimonials,
        'achievements': achievements,
        'highlights': highlights,
    }
    return render(request, 'landing.html', context)
