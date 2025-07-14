from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'first_name', 'last_name', 'year_of_study', 'department', 'email', 'phone_number', 'password']