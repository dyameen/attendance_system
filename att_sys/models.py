import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from enum import Enum

from django.utils import timezone


class SiteUser (AbstractUser):
    role_types = (("Admin","Admin"),("HR","HR"),("NormalUser","NormalUser"))
    role = models.CharField(max_length = 15,choices = role_types)

    class Meta (AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
#
# from django.contrib.auth.base_user import BaseUserManager
#
# class CustomUserManager(BaseUserManager):
#
#     def _create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError("The given email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError(
#                 "Superuser must have is_staff=True."
#             )
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError(
#                 "Superuser must have is_superuser=True."
#             )
#
#         return self._create_user(email, password, **extra_fields)
# class AbstractUser(AbstractBaseUser, PermissionsMixin):
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     first_name = models.CharField(_('first name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     email = models.EmailField(_('email address'), blank=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#
#     objects = UserManager()
#
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']



class Employee(models.Model):
    #username = models.CharFi---------eld(max_length = 255)
    #password = models.CharField(max_length = 128 , null = False)
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
    date= models.DateField(default = datetime.date.today())
    #date = models.DateTimeField (default = timezone.now())
    chin= models.TimeField()
    chout= models.TimeField()
    remarks = models.CharField(max_length = 255,blank = True)
