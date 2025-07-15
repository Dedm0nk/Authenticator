from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'year_of_study', 'department', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = Student(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance