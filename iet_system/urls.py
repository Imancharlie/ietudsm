"""
URL configuration for iet_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import shutil
from datetime import datetime

@login_required
def download_database_backup(request):
    """Download SQLite database backup (admin/staff only)."""
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    db_path = settings.BASE_DIR / 'db.sqlite3'
    if not os.path.exists(db_path):
        return HttpResponse("Database file not found", status=404)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"ietudsm_backup_{timestamp}.sqlite3"
    
    # Read database file
    with open(db_path, 'rb') as f:
        db_data = f.read()
    
    response = HttpResponse(db_data, content_type='application/x-sqlite3')
    response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
    return response

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
    path('admin-panel/', include('system_config.urls')),
    path('admin/backup-db/', download_database_backup, name='backup_database'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


