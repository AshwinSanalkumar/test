from .models import User, UserFile
import hashlib
from django.conf import settings
from rest_framework.exceptions import ValidationError
import mimetypes
from django.shortcuts import get_object_or_404

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
        mime_type, _ = mimetypes.guess_type(file_obj.name)
        mime_type = mime_type or 'application/octet-stream'
        display_name = data.get('display_name') or file_obj.name
        description = data.get('description') or ""
        return UserFile.objects.create(
            owner=user,
            content=file_obj,
            checksum_sha256=checksum,
            file_size_bytes=file_obj.size,
            display_name=display_name,
            original_filename=file_obj.name,
            description=description, 
            mime_type=mime_type
        )
    
    @classmethod
    def update_file_record(cls, file_instance, data, new_file_obj=None):

        if 'display_name' in data:
            file_instance.display_name = data.get('display_name') or file_instance.original_filename
        
        if 'description' in data:
            file_instance.description = data.get('description') or ""

        if new_file_obj:
            if new_file_obj.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError("Replacement file exceeds 100MB limit.")

            file_instance.content = new_file_obj
            file_instance.original_filename = new_file_obj.name
            file_instance.file_size_bytes = new_file_obj.size
            file_instance.checksum_sha256 = cls.calculate_sha256(new_file_obj)
        
            mime, _ = mimetypes.guess_type(new_file_obj.name)
            file_instance.mime_type = mime or 'application/octet-stream'

        file_instance.save()
        file_instance.refresh_from_db()
        return file_instance
    
    @classmethod
    def get_valid_file(cls, file_id, user):
        return get_object_or_404(
            UserFile, 
            pk=file_id, 
            owner=user, 
            is_archived=False
        )