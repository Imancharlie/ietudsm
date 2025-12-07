from django.urls import path
from .views import mark_certificate_ready, update_status_to_processing

app_name = 'certificates'

urlpatterns = [
    path('mark-ready/<int:pk>/', mark_certificate_ready, name='mark_ready'),
    path('update-processing/<int:pk>/', update_status_to_processing, name='update_processing'),
]




