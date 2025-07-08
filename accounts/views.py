from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import CustomRegistrationForm, ProfileEditForm
from accounts.models import Profile

UserModel = get_user_model()


class RegisterView(CreateView):
    # Signal is used to create Profile when new user is registered
    model = UserModel
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')


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


def profile_details(request, pk: int):
    return render(request, 'registration/profile-details-page.html')

def profile_delete(request, pk: int):
    return render(request, 'registration/profile-delete-page.html')