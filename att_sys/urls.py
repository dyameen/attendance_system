from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name = 'index'),
    path("login/",views.loginform,name = "login"),
    path("logout/",views.logout_profile,name = "logout"),
    path("hrprofile/userprofile/<int:id>/",views.user_profile,name = "userprofile"),
    path("hrprofile/userprofile/<int:id>/success",views.success,name = "userprofilesuccess"),
    path("hrprofile/",views.hr_profile,name = "hrprofile"),
    path('hrprofile/delete/<int:id>/',views.delete,name = 'delete'),
    path('hrprofile/userprofile/deleteatt/<int:id>',views.delete_att,name = 'deleteatt'),
    path('hrprofile/userprofile/update/<int:id>',views.update,name = 'update'),
    path("userpersonal/<int:id>/",views.user_personal,name = "userpersonal"),
    path('userpersonal/add/',views.add,name = 'addrecord'),

]
