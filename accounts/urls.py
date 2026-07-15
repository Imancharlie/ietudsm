from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView
from .profile_views import profile, about_us, notifications, settings

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('about/', about_us, name='about'),
    path('notifications/', notifications, name='notifications'),
    path('settings/', settings, name='settings'),
]




