from django import forms

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


def check_chin(value):
    if value == ' ':
        raise forms.ValidationError ("Invalid Check-In Time.")


def check_chout(value):

    if value == ' ':
        raise forms.ValidationError ("Invalid Check-Out Time.")


class Add (forms.ModelForm):
    #chin = forms.TimeField(required = True)

    class Meta:
        model = Attendance
        fields = ('date','chin','chout','remarks')
        widgets = {
            'date': forms.DateInput(attrs = {'type': 'date','readonly':'True'}),
            'chin': forms.TimeInput(attrs = {'type': 'time','required': True}),
            'chout': forms.TimeInput(attrs = {'type': 'time','required': True}),
            'remarks': forms.Textarea(attrs = {'type': 'text','placeholder':"Write your progress here...",'cols': 60,'rows':3,'required': True}),
        }
        labels = {
            'date': 'Date:',
            'chin': 'Check-in Time:',
            'chout': 'Check-out Time:',
            'remarks': "Today's Tasks:"
        }
