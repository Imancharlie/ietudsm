from django.urls import path
from .views import (
    admin_dashboard, system_settings,
    testimonials_list, testimonial_create, testimonial_edit, testimonial_delete,
    achievements_list, achievement_create, achievement_edit, achievement_delete,
    highlights_list, highlight_create, highlight_edit, highlight_delete,
    staff_list, staff_create, staff_edit, staff_delete
)

app_name = 'system_config'

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('settings/', system_settings, name='settings'),
    
    # Testimonials
    path('testimonials/', testimonials_list, name='testimonials'),
    path('testimonials/create/', testimonial_create, name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', testimonial_delete, name='testimonial_delete'),
    
    # Achievements
    path('achievements/', achievements_list, name='achievements'),
    path('achievements/create/', achievement_create, name='achievement_create'),
    path('achievements/<int:pk>/edit/', achievement_edit, name='achievement_edit'),
    path('achievements/<int:pk>/delete/', achievement_delete, name='achievement_delete'),
    
    # Highlights
    path('highlights/', highlights_list, name='highlights'),
    path('highlights/create/', highlight_create, name='highlight_create'),
    path('highlights/<int:pk>/edit/', highlight_edit, name='highlight_edit'),
    path('highlights/<int:pk>/delete/', highlight_delete, name='highlight_delete'),
    
    # Staff
    path('staff/', staff_list, name='staff'),
    path('staff/create/', staff_create, name='staff_create'),
    path('staff/<int:pk>/edit/', staff_edit, name='staff_edit'),
    path('staff/<int:pk>/delete/', staff_delete, name='staff_delete'),
]
