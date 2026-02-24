from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')  # Ensure this matches your urls.py name
        self.valid_payload = {
            "username": "testuser",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }

    def test_registration_success(self):
        """Test that a user can register with valid data."""
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_registration_password_mismatch(self):
        """Test that mismatched passwords return a validation error."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password_confirm'] = "different_password"
        
        response = self.client.post(self.url, invalid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_duplicate_email(self):
        """Test that the custom validate_email prevents duplicate emails."""
        # Create an existing user
        User.objects.create_user(
            username="existing", 
            email="test@example.com", 
            password="password123"
        )
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_missing_fields(self):
        """Test that missing required fields returns 400."""
        payload = {"username": "incomplete"}
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)