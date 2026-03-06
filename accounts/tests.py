from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'bio': 'Test bio',
            'favorite_genres': ['fiction', 'mystery'],
            'reading_goal': 20
        }
    
    def test_user_registration_success(self):
        """Test that user can register with valid data"""
        response = self.client.post(
            self.register_url, 
            self.valid_user_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_user_registration_password_mismatch(self):
        """Test that registration fails when passwords don't match"""
        data = self.valid_user_data.copy()
        data['password2'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', str(response.data))
    
    def test_user_registration_duplicate_username(self):
        """Test that registration fails with existing username"""
        # Create first user
        User.objects.create_user(
            username='testuser',
            email='test1@example.com',
            password='SecurePass123!'
        )
        
        # Try to create another with same username
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', str(response.data))
