from celery import shared_task
from django.db.models import Q
from datetime import datetime
from .models import *
from django.core.mail import send_mail
from django.conf import settings


def send_mail_task(subject,msg,recipient_list):
    send_mail(
            subject = subject,
            message = msg,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [recipient_list],
              )
    return None


@shared_task
def auto_checkout():
    today = str(datetime.datetime.now().date())
    now = datetime.datetime.now()
    att = Attendance.objects.filter(Q(date = today) & Q(chout = None))

    for i in att:
        print("Attendance id =====>",i)
        print ("AutoCheckOut Count =====>",i.employee.autochout)

        if i.employee.autochout <= 3:
            print('In if AutoCheckOut Count =====>',i.employee.autochout)
            Attendance.objects.filter(id=i.id).update(chout = now)
            Employee.objects.filter(id=i.employee.id).update(autochout= i.employee.autochout+1 )
            send_mail_task("Auto CheckOut WARNING!",f"You are auto-checked out {i.employee.autochout} time.",i.employee.eemail)
            print ('auto_checkout task completed !!!')
            return False
        else:
            send_mail_task("Auto CheckOut Action!!!","Since,You are already auto-checked 3 times.Please contact HR-Manager.",i.employee.eemail)
            print("In else: auto checked out 3 times")
    return None


@shared_task
def reload_autochout():
    emp = Employee.objects.filter(autochout__gte = 1)
    for i in emp:
        Employee.objects.filter (id = i.id).update(autochout = 0)
    return None


@shared_task
def auto_reload ():
    print ('auto_reload task completed !!!')
    return None
