from django.urls import path
from .views import confirm_payment, reject_payment

app_name = 'payments'

urlpatterns = [
    path('confirm/<int:pk>/', confirm_payment, name='confirm'),
    path('reject/<int:pk>/', reject_payment, name='reject'),
]




