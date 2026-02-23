from .models import User, UserFile
import hashlib
from django.conf import settings
from rest_framework.exceptions import ValidationError

class AuthService:
    @staticmethod
    def register_user(validated_data: dict) -> User:
        """
        Business Logic: Normalizes data and persists user.
        Note: password_confirm is handled by the serializer, not here.
        """
        return User.objects.create_user(
            email=validated_data['email'].lower().strip(),
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'].strip().capitalize(),
            last_name=validated_data['last_name'].strip().capitalize()
        )
    
#FILE SERVICES
class FileStorageService:
    @staticmethod
    def calculate_sha256(file_obj):
        sha256_hash = hashlib.sha256()
        file_obj.seek(0)
        for chunk in file_obj.chunks(chunk_size=65536):
            sha256_hash.update(chunk)
        file_obj.seek(0)
        return sha256_hash.hexdigest()

    @classmethod
    def process_and_store_file(cls, user, file_obj, data):
        if file_obj.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("File exceeds 100MB limit.")
        checksum = cls.calculate_sha256(file_obj)
        display_name = data.get('display_name') or file_obj.name
        category = data.get('category') or 'General'
        return UserFile.objects.create(
            owner=user,
            content=file_obj,
            checksum_sha256=checksum,
            file_size_bytes=file_obj.size,
            display_name=display_name,
            original_filename=file_obj.name,
            category=category
        )