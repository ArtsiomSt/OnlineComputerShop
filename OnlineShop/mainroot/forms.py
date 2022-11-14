import re
import string
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Users_order, Manufact, Product


class UserSingUp(UserCreationForm):
    username = forms.CharField(max_length=40)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


class UserSignIn(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class UserOrderForm(forms.ModelForm):
    class Meta:
        model = Users_order
        fields = ['users_fio', 'phone_number', 'users_address', 'dest_type']

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        print('Validation')
        allowed = string.digits+'+-'
        for item in value:
            if not item in allowed:
                raise ValidationError("Invalid Phone Number")
        if not re.match(r'[+]?[0-9][ ]?[0-9]*[-]?[0-9][-]?[0-9]', value):
            print('error')
            raise ValidationError("Invalid phone number")
        return value


class FilterForm(forms.Form):
    max_price = forms.IntegerField(required=False)
    min_price = forms.IntegerField(required=False)
    title = forms.CharField(max_length=50, required=False)
    manufactor = forms.ModelChoiceField(queryset=Manufact.objects.all(), required=False)
    title = forms.CharField(max_length=50, required=False)


class EditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'remain_in_stock']
