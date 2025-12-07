from django.urls import path
from .views import create_application, application_status, staff_application_list, staff_application_detail, application_preview
from .staff_views import staff_dashboard

app_name = 'applications'

urlpatterns = [
    path('create/', create_application, name='create'),
    path('preview/', application_preview, name='preview'),
    path('status/', application_status, name='status'),
    path('staff/', staff_application_list, name='staff_list'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('staff/<int:pk>/', staff_application_detail, name='staff_detail'),
]




