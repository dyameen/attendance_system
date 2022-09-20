from django.contrib import admin

# Register your models here.
from .models import *


@admin.register (SiteUser)
class SiteUSerAdmin (admin.ModelAdmin):
    list_display = ('id','username','role')

@admin.register (Employee)
class EmployeeAdmin (admin.ModelAdmin):
    list_display = ('id','user','designation')

@admin.register (Attendance)
class AttAdmin (admin.ModelAdmin):
    list_display = ('id','employee','chin','chout')




#admin.site.register (SiteUser)
#admin.site.register (Employee)
#admin.site.register (Attendance)
