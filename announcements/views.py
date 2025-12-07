from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Announcement
from .forms import AnnouncementForm


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/list.html'
    context_object_name = 'announcements'
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True).order_by('-created_at')


class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/form.html'
    success_url = reverse_lazy('announcements:list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Announcement created successfully.')
        return super().form_valid(form)


class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/form.html'
    success_url = reverse_lazy('announcements:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Announcement updated successfully.')
        return super().form_valid(form)


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcements/delete.html'
    success_url = reverse_lazy('announcements:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Announcement deleted successfully.')
        return super().delete(request, *args, **kwargs)




