import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import forms
from .models import *


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



def index(request):
    return render(request, "index.html")


@csrf_exempt
def loginform(request):
    print('In loginform =====>')
    if request.method == "POST":
        print('In Login if =====>')
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            print('LoginForm is valid  =====>')
            un = fm.cleaned_data['username']
            pwd = fm.cleaned_data['password']
            user = authenticate(username=un, password=pwd)

            if user is not None:
                print("User id is =====> ", user.id)
                login(request, user)
                print("After login User role is =====> ", user.role)
                messages.success(request, "login Successful!")
                if request.user.role == "Admin":
                    return HttpResponseRedirect('/admin/')
                elif request.user.role == "HR":
                    return HttpResponseRedirect('/att_sys/hrprofile/')
                else:
                    emp = Employee.objects.get(user = request.user.id)
                    return HttpResponseRedirect(f"/att_sys/userpersonal/{emp.id}")
    else:
        fm = AuthenticationForm()
        print('In Login else =====>')
    return render(request, 'login.html', {'form': fm})


@csrf_exempt
def logout_profile(request):
    print("In logout  =====>")
    logout(request)
    return render(request, "index.html")


@csrf_exempt
@login_required(login_url="/att_sys/login/")
def hr_profile(request):
    print('In hr_profile =====>')
    user = Employee.objects.exclude(id=1)
    emp = Employee.objects.get(user = request.user.id)
    today = datetime.datetime.now ().date ()
    att = Attendance.objects.filter (Q (employee = emp) & Q (date = today))
    designation = set()
    ename = set ()
    for i in user:
        designation.add(i.designation)
        ename.add (i.ename)
    designation = list(designation)
    print ('Designation =====>',designation)
    ename = list(ename)
    print ('ename =====>',ename)

    if request.method == "POST":
        role = request.POST['role']
        get_ename = request.POST['ename']
        user = Employee.objects.all ()
        print(role)
        print (get_ename)
        if role and get_ename:
            user = Employee.objects.filter (Q (designation = role) & Q (ename = get_ename))
        elif role or get_ename:
            user = Employee.objects.filter (Q (designation = role) | Q (ename = get_ename))

        context = {
            'user': user,
            'designation':designation,
            'emp': emp,
            'att': att,
            'ename': ename,
         }
        return render(request,'hrprofile.html',context)

    elif request.method == 'GET':
        return render(request,'hrprofile.html',
                      {'user': user,'designation':designation,'emp':emp,'att':att,'ename':ename})
    else:
        return HttpResponse('An Exception Occurred')


@login_required(login_url="/att_sys/login/")
def user_profile(request,id):
    print("In user_profile =====> ")
    user = Attendance.objects.filter(employee_id = id).order_by('date')
    emp = Employee.objects.get(id=id)
    print ('Employee in user_profile =====>',emp)
    dwh = {}
    for i in user:
        t1 = i.chin
        t2 = i.chout
        if i.chout and i.chin:
            t1_datetime = datetime.datetime.combine (datetime.datetime.today (),t1)
            t2_datetime = datetime.datetime.combine (datetime.datetime.today (),t2)
            diff = t2_datetime - t1_datetime
            wh = int (diff.total_seconds () / 3600)
            dwh[i.id] = wh

        else:
            wh = 0
            dwh[i.id] = wh

    twh = sum (dwh.values ())
    context = {
        'user': user,
        'name': request.user,
        'emp': emp,
        'dwh': dwh,
        'twh': twh,
    }
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        print(fromdate,todate)
        user = Attendance.objects.filter(Q(employee_id = id) & Q(date__gte=fromdate) & Q(date__lte=todate)).order_by('date')
        print(user,'=====>')
        context['user'] = user
        print(context)
        return render(request, "userprofile.html", context)
    else:
        context['user'] = user
        return render(request, "userprofile.html", context)


@login_required(login_url="/att_sys/login/")
def update(request,id):
    print ("In update =====>")
    att = Attendance.objects.get(id = id)
    emp = Employee.objects.get(id=att.employee.id)
    print('Employee in update =====>',emp)
    id_user = att.employee.id
    if request.method == "POST":
        fm = forms.Update(request.POST)
        print ('POST Update form =====>',fm)
        if fm.is_valid():
            print ('UpdateForm is valid  =====>')
            date = request.POST['date']
            chin = request.POST['chin']
            chout = request.POST['chout']
            user = Attendance(id=id, employee = emp,date = date,chin = chin,chout =chout)
            user.save()
            messages.success(request,"Successfully Updated!")
            return HttpResponseRedirect(f"/att_sys/hrprofile/userprofile/{id_user}")
    else:
        fm = forms.Update(instance = att)
        print('GET Update form =====>',fm)
    return render(request,"update.html",{'name': request.user,'form': fm, 'id_user':id_user})


@login_required(login_url="/att_sys/login/")
def delete(id):
    print('In delete =====>')
    user = Employee.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('hrprofile'))


@login_required(login_url="/att_sys/login/")
def delete_att(id):
    print('In delete_att =====>')
    att = Attendance.objects.get(id=id)
    id_user = att.employee.id
    print(id_user)
    att.delete()
    return HttpResponseRedirect(f'/att_sys/hrprofile/userprofile/{id_user}/')


@login_required(login_url="/att_sys/login/")
def add(request):
        print('In add =====>')
        today = datetime.datetime.now ().date ()
        emp = Employee.objects.get(user = request.user)
        print('Employee in add =====>',emp)
        print('Role in add =====>',emp.user.role)
        att = Attendance.objects.filter(Q(employee = emp.id) & Q(date = today))
        if request.method == "POST":
            fm = forms.Add(request.POST)
            print ('Form in add POST =====>',fm)
            if fm.is_valid ():
                print ('AddForm is valid  =====>')
                date = request.POST.get ('date')
                chin = request.POST.get ('chin')
                chout = request.POST.get ('chout')
                if att:
                    for i in att:
                        print("In checkout =====>")
                        Attendance.objects.filter(id=i.id).update(chout=chout)
                else:
                    print ("In checkin =====>")
                    user = Attendance (employee = emp,date = date,chin = chin)
                    user.save ()
                messages.success (request,"Successfully Add!")
                return HttpResponseRedirect (f'/att_sys/userpersonal/{emp.id}',{'form': fm,'att':att})

        else:
            fm = forms.Add ()
        return render (request,"add.html",{'name': request.user,'form': fm,'emp': emp,'att':att})


@login_required(login_url="/att_sys/login/")
def user_personal(request,id):
    print ("In user_personal =====>")
    today = datetime.datetime.now ().date ()
    emp = Employee.objects.get(user = request.user)
    print ('Employee in user_personal =====>',emp)
    att = Attendance.objects.filter (Q (employee = emp) & Q (date = today))

    if emp.id == id:
        user = Attendance.objects.filter(employee_id = id).order_by('date')
        dwh = {}
        for i in user:
            t1 = i.chin
            t2 = i.chout
            if i.chout and i.chin:
                t1_datetime = datetime.datetime.combine(datetime.datetime.today (),t1)
                t2_datetime = datetime.datetime.combine(datetime.datetime.today (),t2)
                diff = t2_datetime - t1_datetime
                wh = int (diff.total_seconds () / 3600)
                dwh[i.id] = wh

            else:
                wh = 0
                dwh[i.id] = wh

        twh = sum (dwh.values ())
        context = {
            'user': user,
            'name': request.user,
            'emp': emp,
            'dwh': dwh,
            'twh': twh,
            'att': att,
        }
        return render(request, "userpersonal.html", context)
    else:
        return HttpResponseRedirect('/att_sys/login/')


    # add view using session

        # session = request.session['count']
        # emp = Employee.objects.get(user = request.user)
        # print(emp.user.role)
        # if request.method == "POST":
        #     fm = forms.Add(request.POST)
        #     print(fm)
        #
        #     if fm.is_valid():
        #         date = request.POST.get('date')
        #         chin = request.POST.get('chin')
        #         chout = request.POST.get('chout')
        #         if session == 0:
        #             user = Attendance(employee = emp,date = date,chin = chin)
        #             id = user.id
        #             print(id)
        #             message = "Checked in successfully!"
        #         else:
        #             att = Attendance.objects.last()
        #             id = att.id
        #             user = Attendance (id=id,employee = emp,date = date,chin= att.chin,chout = chout)
        #             message = "Checked out successfully!"
        #         user.save ()
        #         messages.success (request,message)
        #         return HttpResponseRedirect(f'/att_sys/userpersonal/{emp.id}',{'form': fm,'session':session})
        #
        # else:
        #     fm = forms.Add()
        #     print(fm)
        # return render (request,"add.html",{'name': request.user,'form': fm ,'emp':emp,'session':session})


# hr_profile without checkin implementation

        # @csrf_exempt
        # @login_required(login_url="/att_sys/login/")
        # def hr_profile(request):
        #     user = Employee.objects.exclude(id=1)
        #     designation = set()
        #     for i in user:
        #         designation.add(i.designation)
        #     designation = list(designation)
        #     emp = Employee.objects.get(user = request.user.id)
        #     print(user)
        #     print("In HR profile")
        #     context = {
        #         'user': user,
        #         'emp': emp,
        #         "designation":designation,
        #     }
        #     return render(request, "hrprofile.html", context)

# loginform using session

        # get_user = SiteUser.objects.get(username = un)
        # last_login_date = get_user.last_login

        # today = datetime.datetime.now().date()
        # print("today =====>",today)
        # print("last_login =====>",last_login_date.date())
        # if last_login_date.date() == today:
        #     request.session['count'] = 1
        #     request.session.modified = True
        # else:
        #     request.session['count'] = 0
        #     request.session.modified = True

def test_vue(request,id):
    print ("In user_personal =====>")
    today = datetime.datetime.now ().date ()
    emp = Employee.objects.get (user = request.user)
    print ('Employee in user_personal =====>',emp)
    att = Attendance.objects.filter (Q (employee = emp) & Q (date = today)).values()
    data = [i for i in att]

    for i in data:
        i["date"] = str(i["date"])
        i["chin"] = str (i["chin"])
        i["chout"] = str (i["chout"])

    att = json.dumps(data)
    print('data ---------------->',data)
    print('------------------>attttttttttt',att)
    if emp.id == id:
        user = Attendance.objects.filter (employee_id = id).order_by ('date').values ()
        user_data = [i for i in user]

        for i in user_data:
            i["date"] = str (i["date"])
            i["chin"] = str (i["chin"])
            i["chout"] = str (i["chout"])

        user = json.dumps(user_data)
        print('userrrrrrrrrrrrrrrrrrrrrrrr---------------->',user)
        user = json.loads(user)
        print('nnnnnnnnnnnnnnnnnnnnnnnnnnn=====>', user)
        dwh = {}
        for i in user:
            t1 = i['chin']
            t2 = i['chout']
            # import dateutil.parser
            # t1 = dateutil.parser.parse (t1)
            # t2 = dateutil.parser.parse (t2)
            t1 = datetime.datetime.strptime (t1,"%H:%M:%S")
            t2 = datetime.datetime.strptime (t2,"%H:%M:%S")
            if i['chin'] and i['chin']:
                t1_datetime = datetime.datetime.combine (datetime.datetime.today (),t1.time())
                t2_datetime = datetime.datetime.combine (datetime.datetime.today (),t2.time())
                diff = t2_datetime - t1_datetime
                wh = int (diff.total_seconds () / 3600)
                dwh[i['id']] = wh

            else:
                wh = 0
                dwh[i['id']] = wh

        twh = sum (dwh.values ())
        context = {
            'user': user,
            'name': request.user,
            'emp': emp,
            'dwh': dwh,
            'twh': twh,
            'att': att,
        }
        return render (request,'vue_app/test.html')
    else:
        return render (request,'vue_app/test.html')

