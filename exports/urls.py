from django.urls import path
from .views import export_application_form, bulk_export_form, bulk_export_zip

app_name = 'exports'

urlpatterns = [
    path('application/<int:pk>/', export_application_form, name='application_form'),
    path('bulk/', bulk_export_form, name='bulk_export_form'),
    path('bulk/zip/', bulk_export_zip, name='bulk_export_zip'),
]




