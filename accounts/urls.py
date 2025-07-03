from django.contrib.auth.views import LoginView
from django.urls import path, include

from accounts import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(form_class=CustomLoginForm), name='login'),
    path('prifile/<int:pk>', include([
        path('', views.profile_details, name='profile-details'),
        path('edit/', views.profile_edit, name='profile-edit'),
        path('delete/', views.profile_delete, name='profile-delete')
    ]))
]