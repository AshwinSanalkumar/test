from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=150)
    email=serializers.EmailField()
    first_name=serializers.CharField(max_length=150)
    last_name=serializers.CharField(max_length=150)
    password=serializers.CharField(write_only=True, min_length=8)
    password_confirm=serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['password'] !=data['password_confirm']:
            raise serializers.ValidationError({"password":"Passwords does not match."})
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value