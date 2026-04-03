from rest_framework import serializers
from .models import Book, ReadingList, Review
from accounts.serializers import UserListSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('average_rating', 'total_reviews', 'created_at', 'updated_at')

class BookListSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'cover_image', 'average_rating', 'total_reviews')

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

class ReviewSerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'likes')

class ReviewDetailSerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)
    book_details = BookSerializer(source='book', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class BookDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='total_reviews', read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'

# Add to books/serializers.py
class ReadingListSerializer(serializers.ModelSerializer):
    book_details = BookListSerializer(source='book', read_only=True)
    reading_progress = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ReadingList
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class ReadingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ('book', 'status', 'current_page', 'started_at', 'completed_at', 'personal_notes')
    
    def validate(self, data):
        # Custom validation logic
        if data.get('status') == 'read' and not data.get('completed_at'):
            data['completed_at'] = data.get('started_at')
        return data
    
class BookCoverUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['cover_image']