from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile

UserModel = get_user_model()


class CustomRegistrationForm(UserCreationForm):

    # In the Base form only username field is set so we add the other fields in the form
    email = forms.EmailField(
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email' ,'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username...',
            'autofocus': False,
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email...'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password...'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Re-enter password...'
        })

class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username/Email',
            'autofocus': False,
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })


class BaseProfileForm(forms.ModelForm):
    DEFAULT_STYLE = 'flex-1 px-3 py-1 border border-pink-200 rounded-md outline-none focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent'
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': DEFAULT_STYLE,
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': DEFAULT_STYLE,
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': DEFAULT_STYLE,
        })
    )

    class Meta:
        model = Profile
        fields = ('location', 'profile_picture')
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'flex-1 px-3 py-1 border border-pink-200 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'block mx-auto mt-2 text-sm text-pink-600 file:mr-4 file:py-2 file:px-4 file:rounded-full'
                         ' file:border-0 file:text-sm file:font-semibold file:bg-pink-50 file:text-pink-700 hover:file:bg-pink-100'
            })
        }

class ProfileEditForm(BaseProfileForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user is not None:
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.email = self.cleaned_data.get('email', '')
        self.user.first_name = self.cleaned_data.get('first_name', '')
        self.user.last_name = self.cleaned_data.get('last_name', '')

        if commit:
            self.user.save()
            profile.save()

        return profile

