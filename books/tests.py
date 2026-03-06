from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book, Review

User = get_user_model()

class BookTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'genre': 'fiction',
            'publication_year': 2024,
            'description': 'A test book description'
        }
        self.book = Book.objects.create(**self.book_data)
    
    def test_list_books(self):
        """Test that anyone can list books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_book_authenticated(self):
        """Test that authenticated user can create book"""
        self.client.force_authenticate(user=self.user)

        new_data = self.book_data.copy()
        new_data['isbn'] = '9876543210987' 
        
        response = self.client.post('/api/books/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated user cannot create book"""
        response = self.client.post('/api/books/', self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)