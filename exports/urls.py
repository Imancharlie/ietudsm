from django.urls import path
from .views import export_application_form

app_name = 'exports'

urlpatterns = [
    path('application/<int:pk>/', export_application_form, name='application_form'),
]




