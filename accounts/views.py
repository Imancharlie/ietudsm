from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserSignUpForm


class SignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('applications:create')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            # Staff members go to staff dashboard, not application form
            return reverse_lazy('applications:staff_dashboard')
        elif user.has_completed_application:
            if user.is_approved_member:
                return reverse_lazy('dashboard:index')
            else:
                return reverse_lazy('applications:status')
        else:
            return reverse_lazy('applications:create')


class CustomLogoutView(LogoutView):
    next_page = 'landing'




