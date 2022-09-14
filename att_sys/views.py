from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from .models import *
from . import forms
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


def index (request):
    return render (request,"index.html")


# def login_request (request):
#     su = SiteUser.objects.
#     return render (request,"login.html")


# Create your views here.
def loginform (request):
    form = forms.Login()
    if request.method == 'POST':
        form = forms.Login(request.POST)
        html = 'You are already logged in'
        if form.is_valid():
            html = html + " :The Credentials are Valid."
    else:
        html = 'Login for first time'
    return render (request,'login.html',{'html': html,'form': form})
