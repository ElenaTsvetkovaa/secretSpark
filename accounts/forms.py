from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

UserModel = get_user_model()


class CustomRegistrationForm(UserCreationForm):

    # In the Base form only username field is set so we add the other fields in the form
    first_name = forms.CharField(
        max_length=100,
        required=True,
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
    )
    email = forms.EmailField(
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('first_name', 'last_name', 'email' ,'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name...'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name...'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username...'
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
            'placeholder': 'Username/Email'
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })