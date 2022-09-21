import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from enum import Enum

from django.utils import timezone


class SiteUser(AbstractUser):
    role_types = (("Admin","Admin"),("HR","HR"),("NormalUser","NormalUser"))
    role = models.CharField(max_length = 15,choices = role_types)

    class Meta (AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Employee(models.Model):
    user = models.ForeignKey(SiteUser,on_delete = models.CASCADE,related_name = 'us_employee')
    joindate = models.DateField()
    birthdate = models.DateField()
    age = models.IntegerField()
    designation = models.CharField(max_length = 255)
    ename = models.CharField(max_length = 100)
    eemail = models.EmailField(max_length = 255,blank = False,unique = True)
    city = models.CharField(max_length = 255)

    def __str__ (self):
        return self.ename


class Attendance(models.Model):
    employee = models.ForeignKey(Employee,on_delete = models.CASCADE, related_name = 'emp_attendance')
    date = models.DateField(default = datetime.date.today())
    chin = models.TimeField()
    chout = models.TimeField()
    remarks = models.CharField(max_length = 255,blank = True)
