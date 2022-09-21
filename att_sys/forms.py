from django import forms
from django.contrib.auth import authenticate
from django.core import validators

from .models import *
from django.contrib.auth.forms import AuthenticationForm


class Login (AuthenticationForm):
    class Meta:
        model = SiteUser
        fields = ('username','password')


class Update (forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date','chin','chout')
        widgets = {
            'date': forms.DateInput(attrs = {'type': 'date'}),
            'chin': forms.TimeInput(attrs = {'type': 'time'}),
            'chout': forms.TimeInput(attrs = {'type': 'time'}),
        }
        labels = {
            'date': 'Date:',
            'chin': 'Check-in Time:',
            'chout': 'Check-out Time:',
        }


class Add (forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date','chin','chout')
        widgets = {
            'date': forms.DateInput (attrs = {'type': 'date'}),
            'chin': forms.TimeInput (attrs = {'type': 'time'}),
            'chout': forms.TimeInput (attrs = {'type': 'time'}),
        }
        labels = {
            'date': 'Date:',
            'chin': 'Check-in Time:',
            'chout': 'Check-out Time:',
        }
