from django.contrib import admin
from .models import *


@admin.register (SiteUser)
class SiteUSerAdmin (admin.ModelAdmin):
    list_display = ('id','username','role')


@admin.register (Employee)
class EmployeeAdmin (admin.ModelAdmin):
    list_display = ('id','user','designation','autochout')


@admin.register (Attendance)
class AttAdmin (admin.ModelAdmin):
    list_display = ('id','employee','date','chin','chout','remarks')
