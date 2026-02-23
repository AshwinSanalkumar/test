from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewTests(APITestCase):
    """
    Test suite for RegisterView.
    Designed for software engineering promotion review.
    """

    def setUp(self):
        # Ensure 'register' matches the 'name=' parameter in your urls.py
        self.register_url = reverse('register')
        
        # Payload includes all fields required by your Serializer
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
        """
        Unit Test: Tests the view logic in isolation.
        Uses MagicMock to prevent RecursionError during JSON serialization.
        """
        # Arrange: Setup a mock user object with explicit attributes
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.first_name = "John"
        mock_user.email = "john.doe@example.com"
        
        # Configure the service to return our mock user
        mock_register_user.return_value = mock_user

        # Act
        response = self.client.post(self.register_url, self.valid_payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "success")
        self.assertEqual(response.data['data']['email'], "john.doe@example.com")
        
        # Verify the service was actually called
        mock_register_user.assert_called_once()

    def test_register_user_invalid_data(self):
        """
        Unit Test: Tests that the serializer correctly catches missing data.
        """
        # Arrange: Payload missing the required username
        invalid_payload = self.valid_payload.copy()
        del invalid_payload['username']

        # Act
        response = self.client.post(self.register_url, invalid_payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_integration(self):
        """
        Integration Test: Tests the full flow from View to Database.
        This ensures the AuthService logic is actually compatible with the DB.
        """
        # Act
        response = self.client.post(self.register_url, self.valid_payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="john.doe@example.com").exists())