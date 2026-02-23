from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserFile 
import uuid

User = get_user_model()

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_payload = {
            "username": "testuser_dev",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!"
        }

    @patch('myapp.services.AuthService.register_user')
    def test_register_user_success(self, mock_register_user):
        mock_user = MagicMock(id=1, email="john.doe@example.com", first_name="John")
        mock_register_user.return_value = mock_user

        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "success")

    def test_register_password_mismatch(self):
        """Edge Case: Ensure validation fails if passwords don't match."""
        payload = self.valid_payload.copy()
        payload['password_confirm'] = "WrongPassword123!"
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="devuser@example.com",
            username="devuser",
            password="password123"
        )
        self.other_user = User.objects.create_user(
            email="hacker@example.com",
            username="hacker",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.upload_url = reverse('file-upload')
        self.list_url = reverse('file-list')
    
    @patch('myapp.services.FileStorageService.process_and_store_file')
    def test_file_upload_success(self, mock_storage):
        dummy_file = SimpleUploadedFile("test_doc.txt", b"content", content_type="text/plain")
        

        class FileStub:
            id = uuid.uuid4()
            display_name = "test_doc.txt"  
            original_filename = "test_doc.txt"
            file_size_bytes = 2048
            description = "General"
            checksum_sha256 = "d7a8fbb307d7809469ca9abcb3c0bb21"
            is_archived = False
            content = MagicMock()
            content.url = "/media/vault/test_doc.txt"

        mock_storage.return_value = FileStub()

        response = self.client.post(self.upload_url, {'file': [dummy_file]}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['uploaded'][0]['display_name'], "test_doc.txt")

    def test_upload_no_file_error(self):
        """Edge Case: User hits upload endpoint without a file."""
        response = self.client.post(self.upload_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_file_list_ownership(self):
        """Security: Ensure user only sees their own active files."""

        UserFile.objects.create(owner=self.user, original_filename="my_file.txt", file_size_bytes=10)

        UserFile.objects.create(owner=self.other_user, original_filename="stolen.txt", file_size_bytes=10)

        UserFile.objects.create(owner=self.user, original_filename="old.txt", is_archived=True, file_size_bytes=10)

        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['original_filename'], "my_file.txt")

    def test_get_detail_forbidden_or_archived(self):
        """Security: Prevent access to other users' files or archived files."""
        other_file = UserFile.objects.create(owner=self.other_user, original_filename="secret.txt", file_size_bytes=10)
        archived_file = UserFile.objects.create(owner=self.user, original_filename="deleted.txt", is_archived=True, file_size_bytes=10)


        url_other = reverse('file-detail', kwargs={'pk': other_file.pk})
        res_other = self.client.get(url_other)
        self.assertEqual(res_other.status_code, status.HTTP_404_NOT_FOUND)


        url_archived = reverse('file-detail', kwargs={'pk': archived_file.pk})
        res_archived = self.client.get(url_archived)
        self.assertEqual(res_archived.status_code, status.HTTP_404_NOT_FOUND)

    def test_file_soft_delete_success(self):
        file_record = UserFile.objects.create(owner=self.user, original_filename="bye.txt", file_size_bytes=10)
        url = reverse('file-delete', kwargs={'pk': file_record.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        file_record.refresh_from_db()
        self.assertTrue(file_record.is_archived)

    @patch('myapp.services.FileStorageService.update_file_record')
    def test_file_update_success(self, mock_update):
        """Test partial and full updates of a file record."""
        # 1. Create a real file record in the DB to update
        existing_file = UserFile.objects.create(
            owner=self.user, 
            original_filename="old_file.txt", 
            file_size_bytes=100,
            display_name="Old Version"
        )
        url = reverse('file-update', kwargs={'pk': existing_file.pk})

        # 2. Mock the service return value for a successful update
        class UpdatedFileStub:
            id = existing_file.pk
            display_name = "New Version"
            description = "Updated description"
            original_filename = "new_binary.png"  # Filename changed!
            file_size_bytes = 5000               # Size changed!
            mime_type = "image/png"
            checksum_sha256 = "mocked_hash_123"
            created_at = "2026-02-23T06:37:40Z"

        mock_update.return_value = UpdatedFileStub()

        # 3. Prepare payload with a new file
        new_dummy_file = SimpleUploadedFile("new_binary.png", b"new content", content_type="image/png")
        payload = {
            'display_name': 'New Version',
            'description': 'Updated description',
            'file': new_dummy_file
        }

        # 4. Perform the request
        response = self.client.post(url, payload, format='multipart')

        # 5. Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display_name'], "New Version")
        self.assertEqual(response.data['original_filename'], "new_binary.png")
        self.assertEqual(response.data['file_size_bytes'], 5000)
        
        # Verify the service was called with the correct arguments
        mock_update.assert_called_once()    

