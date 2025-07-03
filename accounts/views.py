from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomRegistrationForm

UserModel = get_user_model()


class RegisterView(CreateView):
    model = UserModel
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

def login(request):
    return render(request, 'registration/login.html')

def profile_details(request, pk: int):
    return render(request, 'registration/profile-details-page.html')

def profile_edit(request, pk: int):
    return render(request, 'registration/profile-edit-page.html')

def profile_delete(request, pk: int):
    return render(request, 'registration/profile-delete-page.html')