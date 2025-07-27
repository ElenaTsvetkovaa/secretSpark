from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
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

class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'registration/profile-edit-page.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.object.user})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'registration/profile-details-page.html'
