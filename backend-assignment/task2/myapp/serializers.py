from rest_framework import serializers
from django.contrib.auth.models import User # This uses Django's built-in User

class RegisterSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(max_length=150,required=True)
    last_name=serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True, min_length=8)
    password_confirm=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')    

    def validate(self, data):

        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields must match."})
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value