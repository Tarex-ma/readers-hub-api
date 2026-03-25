from rest_framework import generics, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view, permission_classes
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Review
from .serializers import (
    BookCoverUploadSerializer, BookSerializer, BookListSerializer, BookDetailSerializer,
    ReviewSerializer, ReviewDetailSerializer,BookCoverUploadSerializer
)
from .permissions import IsOwnerOrReadOnly, CanDeleteReview
from .models import ReadingList
from .serializers import ReadingListSerializer, ReadingListCreateSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .filters import BookFilter
from rest_framework.parsers import MultiPartParser, FormParser
from .services.recommendations import RecommendationService
from django.db.models import Q, Count, Avg
import random


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'author']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'publication_year', 'average_rating']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'spoiler']
    ordering_fields = ['created_at', 'rating']
    
    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id).select_related('user', 'book')
    
    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs['book_id'])
        serializer.save(user=self.request.user, book=book)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewDetailSerializer
        return ReviewSerializer
    
    def perform_update(self, serializer):
        serializer.save()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_review(request, pk):
    """
    Like or unlike a review.
    """
    review = get_object_or_404(Review, id=pk)
    
    if request.user in review.likes.all():
        # Unlike
        review.likes.remove(request.user)
        message = 'Review unliked'
    else:
        # Like
        review.likes.add(request.user)
        message = 'Review liked'
    
    return Response({
        'message': message,
        'likes_count': review.likes.count()
    })

class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(user_id=user_id).select_related('book')


class ReadingListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReadingListSerializer
    
    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        if ReadingList.objects.filter(user=self.request.user, book_id=book_id).exists():
            raise ValidationError({'book': 'This book is already in your reading list'})
        serializer.save(user=self.request.user)

class ReadingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReadingListSerializer
    
    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

class UserReadingListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReadingListSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return ReadingList.objects.filter(user_id=user_id)
    

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description', 'isbn']
    ordering_fields = ['title', 'publication_year', 'average_rating', 'created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer
    
    """
     List all books or create a new book.
    
    - Authentication is required for creating books
    - Supports filtering, searching, and pagination
    
    Query Parameters:
    - `genre`: Filter by genre (e.g., ?genre=fiction)
    - `min_rating`: Minimum average rating (e.g., ?min_rating=4)
    - `search`: Search in title, author, description
    - `ordering`: Sort by field (e.g., ?ordering=-average_rating)
    - `page`: Page number for pagination
    - `page_size`: Number of items per page (default: 10, max: 100)
    
    Returns:
    - List of books with pagination metadata
    """
    # ... view code ...
    

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'spoiler', 'user']
    search_fields = ['text']
    ordering_fields = ['created_at', 'rating', 'likes_count']
    
    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id).select_related('user', 'book')
    
    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs['book_id'])
        serializer.save(user=self.request.user, book=book)

class BookCoverUploadView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCoverUploadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_update(self, serializer):
        # You could add validation here
        serializer.save()


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        limit = int(request.query_params.get('limit', 10))
        
        # Get user's reading history
        read_books = user.reading_list.filter(status='read').values_list('book_id', flat=True)
        
        # Get user's favorite genres
        favorite_genres = user.favorite_genre or []
        
        # Get books from favorite genres that user hasn't read
        recommendations = Book.objects.all()
        
        if favorite_genres:
            recommendations = recommendations.filter(genre__in=favorite_genres)
        
        if read_books:
            recommendations = recommendations.exclude(id__in=read_books)
        
        # Annotate with average rating and order
        recommendations = recommendations.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating', '-total_reviews')[:limit]
        
        serializer = BookListSerializer(recommendations, many=True)
        return Response({'recommendations': serializer.data})
