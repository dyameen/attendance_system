from django import forms
from django.contrib.auth import authenticate
from django.core import validators
from django.forms import DateInput,TimeInput

from .models import *
from django.contrib.auth.forms import AuthenticationForm


class Login(AuthenticationForm):
    # username = forms.CharFielAuthenticationFormd (initial = 'username',)
    # password = forms.CharField (widget = forms.PasswordInput,validators = [validators.MinLengthValidator (4)])

    class Meta:
        model = SiteUser
        fields = ('username','password')


class Update(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date','chin','chout')
        widgets ={
            'date': forms.DateInput(attrs={'type': 'date'}),
            'chin': forms.TimeInput(attrs={'type': 'time'}),
            'chout':forms.TimeInput(attrs={'type': 'time'}),
        }


class Add(forms.ModelForm):
    class Meta:
            model = Attendance
            fields = ('date','chin','chout')
            widgets = {
                'date': forms.DateInput(attrs = {'type': 'date'}),
                'chin': forms.TimeInput(attrs = {'type': 'time'}),
                'chout': forms.TimeInput(attrs = {'type': 'time'}),
                }

        # def clean (self,*args,**kwargs):
        #     username = self.cleaned_data.get ('username')
        #     password = self.cleaned_data.get ('password')
        #
        #     if username and password:
        #         user = authenticate (username = username,password = password)
        #         if not user:
        #             raise forms.ValidationError ('This user does not exist')
        #         if not user.check_password (password):
        #             raise forms.ValidationError ('Incorrect password')
        #         if not user.is_active:
        #             raise forms.ValidationError ('This user is not active')
        #     return super (Login,self).clean (*args,**kwargs)

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
