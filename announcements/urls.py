from django.urls import path
from .views import (
    AnnouncementListView,
    AnnouncementCreateView,
    AnnouncementUpdateView,
    AnnouncementDeleteView
)

app_name = 'announcements'

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='list'),
    path('create/', AnnouncementCreateView.as_view(), name='create'),
    path('<int:pk>/update/', AnnouncementUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='delete'),
]




