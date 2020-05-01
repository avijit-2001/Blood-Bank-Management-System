from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=30, required=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class HospitalSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
