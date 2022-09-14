from django import forms
from django.core import validators
from .models import *


class Login (forms.ModelForm):
    # username = forms.CharField (initial = 'username',)
    password = forms.CharField (widget = forms.PasswordInput,validators = [validators.MinLengthValidator (4)])
    class Meta:
        model= Employee
        fields = ['eemail','password']


    # def clean_password (self):
    #     password = self.cleaned_data['password']
    #     if len (password) < 4:
    #         raise forms.ValidationError ("password is too short")
    #     return password
    #
    # def clean_age(self):
    #     age = self.cleaned_data['age']
    #     print("age from function---",age)
    #     if age > 100 or age<=0:
    #     # if 100 < age <= 0:
    #         raise forms.ValidationError("Enter proper age.")
    #     return age
    #
    # def clean_fav_no(self):
    #
    #     fno = self.cleaned_data['fav_no']
    #     print(fno)
    #     if fno > 100:
    #         raise forms.ValidationError('Enter properly')
    #     return fno
