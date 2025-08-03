from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import CustomRegistrationForm, ProfileEditForm, CustomLoginForm
from accounts.models import Profile

UserModel = get_user_model()


class RegisterView(CreateView):
    # Signal is used to create Profile when new user is registered
    model = UserModel
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url

        profile = Profile.objects.get(user_id=self.request.user.pk)
        return reverse_lazy('profile-details', kwargs={'pk': profile.pk})

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'registration/profile-edit-page.html'

    def get_object(self, queryset = ...):
        return Profile.objects.get(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.object.user})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})



class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'registration/profile-details-page.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You can only view your own profile.")
        return obj
