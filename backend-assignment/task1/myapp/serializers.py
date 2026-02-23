from rest_framework import serializers
from .models import User ,UserFile

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
    
#FILE SERVICE

class UserFileSerializer(serializers.ModelSerializer):
    size_readable = serializers.SerializerMethodField()

    class Meta:
        model = UserFile
        fields = [
            'id', 
            'display_name', 
            'description', 
            'original_filename', 
            'file_size_bytes', 
            'size_readable', 
            'checksum_sha256', 
            'created_at'
        ]
        read_only_fields = [
            'id', 
            'original_filename', 
            'file_size_bytes', 
            'checksum_sha256', 
            'created_at'
        ]

    def get_size_readable(self, obj):
        """
        Converts raw bytes into a human-readable format (KB, MB, GB).
        """
        num = obj.file_size_bytes
        for unit in ['B', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return f"{num:.2f} {unit}"
            num /= 1024.0
        return f"{num:.2f} TB"