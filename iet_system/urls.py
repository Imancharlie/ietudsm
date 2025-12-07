"""
URL configuration for iet_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('accounts/', include('accounts.urls')),
    path('applications/', include('applications.urls')),
    path('payments/', include('payments.urls')),
    path('certificates/', include('certificates.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('announcements/', include('announcements.urls')),
    path('exports/', include('exports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

