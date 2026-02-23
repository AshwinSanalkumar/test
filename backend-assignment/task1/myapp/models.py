from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import os
import uuid
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be provided')
        email= self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)
    
class User(AbstractUser):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    
    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    def __str__(self):
        return self.email
    
#FILE STORAGE

def get_file_storage_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(f'vault/user_{instance.owner.id}', f"{uuid.uuid4()}.{ext}")

class UserFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.FileField(upload_to=get_file_storage_path)
    checksum_sha256 = models.CharField(max_length=64)
    file_size_bytes = models.BigIntegerField()
    
    display_name = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) # Changed from category
    mime_type = models.CharField(max_length=100, editable=False)
    is_archived = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)