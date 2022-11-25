import re
import string
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Users_order, Manufact, Product, Videocard, Proccessor, Memory, Computer, Category, Manufact


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


class CreateComputerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for videocard in Videocard.objects.filter(remain_in_stock__gt=1):
            choices.append((videocard.pk, videocard))
        self.fields['videocard'].choices = choices
        choices.clear()
        for processor in Proccessor.objects.filter(remain_in_stock__gt=1):
            choices.append((processor.pk, processor))
        self.fields['processor'].choices = choices
        choices.clear()
        for memory in Memory.objects.filter(remain_in_stock__gt=1):
            choices.append((memory.pk, memory))
        self.fields['memory_p'].choices = choices
        return

    title = forms.CharField(max_length=100)
    price = forms.IntegerField()
    gabs = forms.CharField(max_length=100, label='Size')
    videocard = forms.ChoiceField()
    processor = forms.ChoiceField()
    memory_p = forms.ChoiceField()

    def save(self):
        validated_data = {}
        if self.is_valid():
            for key,value in self.cleaned_data.items():
                if key == 'videocard':
                    validated_data[key] = Videocard.objects.get(pk=value)
                elif key == 'processor':
                    validated_data[key] = Proccessor.objects.get(pk=value)
                elif key == 'memory_p':
                    validated_data[key] = Memory.objects.get(pk=value)
                else:
                    validated_data[key] = value
            validated_data['manuf'] = Manufact.objects.get(pk=1)
            return Computer.objects.create(**validated_data, remain_in_stock=1, amount_ordered=0, category=Category.objects.get(title='PC'))
