from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserSingUp(UserCreationForm):
    username = forms.CharField(max_length=40)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


class UserSignIn(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
