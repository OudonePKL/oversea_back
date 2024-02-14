from .models import UserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm  # Edit user profile
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput, Textarea, DateInput, ClearableFileInput


# from django.contrib.auth import get_user_model


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ['nickname', 'email', 'password',]

        widgets = {
            'nickname': TextInput(attrs={
                'class': "form-control",  # Required for bootstrap application!
                'placeholder': 'Nickname'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
            'code': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Code'
            }),
            'password': PasswordInput(attrs={
                'class': "form-control",
                'style': "font-family: sans-serif",
                'placeholder': 'Password'
            }),
        }
