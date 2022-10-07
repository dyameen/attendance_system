from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *


# User Serializer
class LoginSerializer (serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ['username','password']

    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')


# Register Serializer
# class EmployeeSerializer (serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'
#
#
class AttendanceSerializer (serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

#     def create (self,validated_data):
#         return Attendance.objects.create (**validated_data)
#
#     def update (self,instance,validated_data):
#         instance.employee = validated_data.get ('employee',instance.employee)
#         instance.date = validated_data.get ('date',instance.date)
#         instance.chin = validated_data.get ('chin',instance.chin)
#         instance.chout = validated_data.get ('chout',instance.chout)
#         instance.remarks = validated_data.get ('remarks',instance.remarks)
#         instance.save ()
#         return instance
#
#
