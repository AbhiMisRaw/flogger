from django import forms
from django.core import validators
from django.contrib.auth import get_user_model

from .constants import Error

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 leading-8"
        })
    )
    password = forms.CharField(
        validators=[validators.MinLengthValidator(4)],
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 leading-6"
        })
    )
    

class UserRegisterForm(forms.Form):
    full_name = forms.CharField(
        label="Full Name",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 leading-8"
        })
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 leading-8"
        })
    )
    password = forms.CharField(
        validators=[validators.MinLengthValidator(6)],
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 text-base leading-6"
        })
    )
    confirm_password = forms.CharField(
        validators=[validators.MinLengthValidator(6)],
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full h-12 px-4 text-base leading-6"
        })
    )

    def clean(self):

        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        is_email_exist = User.objects.filter(email=email).exists()
        if is_email_exist:
            raise forms.ValidationError(Error.USER_EMAIL_EXIST)
        
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("confirm_password")
        if pass1 != pass2:
            raise forms.ValidationError(Error.PASSWORD_MATCHING_ERROR)
