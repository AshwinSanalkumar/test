from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

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

class ArithmeticTests(APITestCase):
    def setUp(self):
        # 1. Create a user for authentication
        self.user = User.objects.create_user(
            username="mathuser", 
            email="math@example.com", 
            password="password123"
        )
        
        # 2. Generate a JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        # 3. Authorize the client for all requests in this class
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_addition_success(self):
        """Test adding two valid numbers."""
        # Pattern: calculate/sum/5/4/
        url = reverse('add-operation', kwargs={'num1': '10.5', 'num2': '4.5'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 15.0)
        self.assertEqual(response.data['operation'], 'sum')

    def test_addition_invalid_input(self):
        """Test adding with non-numeric strings."""
        url = reverse('add-operation', kwargs={'num1': 'abc', 'num2': '5'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_addition_unauthenticated(self):
        """Test that unauthenticated users cannot access the math API."""
        self.client.credentials()  # Wipe the token
        url = reverse('add-operation', kwargs={'num1': '5', 'num2': '5'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)