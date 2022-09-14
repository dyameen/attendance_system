from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class SiteUser (AbstractUser):
    role_types = (("Admin","Admin"),("HR","HR"),("NormalUser","NormalUser"))
    uid = models.AutoField(primary_key = True)
    role = models.CharField(max_length = 15,choices = role_types)

    def __str__ (self):
        return self.role

    class Meta (AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Employee (models.Model):
    uid = models.ForeignKey(SiteUser,on_delete = models.CASCADE)
    joindate = models.DateField()
    birthdate = models.DateField()
    age = models.IntegerField()
    designation = models.CharField(max_length = 255)
    ename = models.CharField(max_length = 100)
    eemail = models.EmailField(max_length = 255,blank = False,unique = True)
    city = models.CharField(max_length = 255)

    def __str__ (self):
        return self.ename


class Attendance (models.Model):
    eid = models.ForeignKey(Employee,on_delete = models.CASCADE)
    date = models.DateField()
    chin = models.TimeField()
    chout = models.TimeField()
    remarks = models.CharField(max_length = 255)

    def __str__ (self):
        return self.eid
