from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .models import *
from . import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import DurationField,ExpressionWrapper,F,IntegerField,Value,Sum
from django.db.models.functions import Coalesce

from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    return render(request, "index.html")


def loginform(request):
    print(request)
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            print('enter')
            un = fm.cleaned_data['username']
            pwd = fm.cleaned_data['password']
            user = authenticate(username=un, password=pwd)
            if user is not None:
                login(request, user)
                emp = Employee.objects.get(user = request.user.id)
                messages.success(request, "login Successful!")
                if request.user.role == "Admin":
                    return HttpResponseRedirect('/admin/')
                elif request.user.role == "HR":
                    return HttpResponseRedirect('/att_sys/hrprofile/')
                else:
                    return HttpResponseRedirect(f"/att_sys/userpersonal/{emp.id}")
    else:
        fm = AuthenticationForm()
        print('In else')
    return render(request, 'login.html', {'form': fm})


@csrf_exempt
def logout_profile(request):
    print("In logout")
    logout(request)
    return render(request, "index.html")


@csrf_exempt
def hr_profile(request):
    user = Employee.objects.exclude(id=1)
    emp = Employee.objects.get(user = request.user.id)
    print(user)
    print("In HR profile")
    context = {
        'user': user,
        'emp': emp,
    }
    return render(request, "hrprofile.html", context)


def user_profile(request,id):
    print("In User profile")
    user = Attendance.objects.filter(employee_id = id).order_by('date')
    emp = Employee.objects.get(id=id)
    dwh = {}
    for i in user:
        t1 = i.chin
        t2 = i.chout
        t1_datetime = datetime.datetime.combine(datetime.datetime.today(),t1)
        t2_datetime = datetime.datetime.combine(datetime.datetime.today(),t2)
        diff = t2_datetime-t1_datetime
        wh = int(diff.total_seconds()/3600)
        dwh[i.id] = wh
    twh = sum(dwh.values())
    context = {
        'user': user,
        'name': request.user,
        'emp': emp,
        'dwh': dwh,
        'twh': twh,
    }
    return render(request, "userprofile.html", context)


def update(request,id):
    print ("In Update")
    att = Attendance.objects.get(id = id)
    emp = Employee.objects.get(id=att.employee.id)
    id_user = att.employee.id
    print(emp,'------>')
    if request.method == "POST":
        fm = forms.Update(request.POST)
        print (fm,'------>')
        if fm.is_valid():
            date = request.POST['date']
            chin = request.POST['chin']
            chout = request.POST['chout']
            user = Attendance(id=id, employee = emp,date = date,chin = chin,chout =chout)
            user.save()
            messages.success(request,"Successfully Updated!")
            return HttpResponseRedirect(f"/att_sys/hrprofile/userprofile/{id_user}")
    else:
        fm = forms.Update(instance = att)
        print(fm)
    return render(request,"update.html",{'name': request.user,'form': fm , 'id_user':id_user})


def success(request, id):
    user = Employee.objects.get(id=id)
    print("In success")
    return render(request, "success.html",{'user':user})


def delete(request, id):
    user = Employee.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('hrprofile'))


def delete_att(request,id):
    att = Attendance.objects.get(id=id)
    id_user = att.employee.id
    print(id_user)
    att.delete()
    return HttpResponseRedirect(f'/att_sys/hrprofile/userprofile/{id_user}/')


def add(request):
    emp = Employee.objects.get(user = request.user)
    if request.method == "POST":
        fm = forms.Add(request.POST)
        print(fm)

        if fm.is_valid():
            date = request.POST.get('date')
            chin = request.POST.get('chin')
            chout = request.POST.get('chout')
            user = Attendance(employee = emp,date = date,chin = chin,chout = chout)
            user.save()
            messages.success (request,"Successfully Add!")
            return HttpResponseRedirect(f'/att_sys/userpersonal/{emp.id}',{'form': fm})

    else:
        fm = forms.Add()
        print(fm)
    return render (request,"add.html",{'name': request.user,'form': fm ,'emp':emp})


def user_personal(request,id):
    emp = Employee.objects.get(user = request.user)
    print("In User profile")
    user = Attendance.objects.filter(employee_id = id).order_by('date')
    print(user,"--------->")
    dwh = {}
    for i in user:
        t1 = i.chin
        t2 = i.chout
        t1_datetime = datetime.datetime.combine(datetime.datetime.today (),t1)
        t2_datetime = datetime.datetime.combine(datetime.datetime.today (),t2)
        diff = t2_datetime - t1_datetime
        wh = int (diff.total_seconds() / 3600)
        dwh[i.id] = wh
    twh = sum (dwh.values ())

    context = {
        'user': user,
        'name': request.user,
        'emp': emp,
        'dwh': dwh,
        'twh': twh,
    }
    return render(request, "userpersonal.html", context)
