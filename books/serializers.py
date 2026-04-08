from rest_framework import serializers
from .models import Book, ReadingList, Review
from accounts.serializers import UserListSerializer
from cloudinary.models import CloudinaryField
# books/serializers.py

class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    reviews_count = serializers.IntegerField(source='total_reviews', read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'genre', 'publication_year', 'publisher',
            'cover_image', 'description', 'page_count',
            'average_rating', 'reviews_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ('average_rating', 'reviews_count', 'created_at', 'updated_at')

    def get_cover_image(self, obj):
        """
        Returns a fully qualified URL for the cover image.
        Works both in local dev (MEDIA_URL) and Cloudinary production.
        """
        if obj.cover_image:
            request = self.context.get('request')
            try:
                # For Cloudinary, this will be an absolute URL already
                url = obj.cover_image.url
            except ValueError:
                return None

            # Build absolute URL for frontend
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class BookListSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(source='total_reviews', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'genre', 'cover_image', 'average_rating', 'reviews_count')

    def get_cover_image(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            url = obj.cover_image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class BookDetailSerializer(BookSerializer):
    """
    Extends BookSerializer with all reviews included.
    """
    reviews = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['reviews']

    def get_reviews(self, obj):
        from .serializers import ReviewSerializer
        reviews = obj.reviews.all().select_related('user')
        serializer = ReviewSerializer(reviews, many=True, context=self.context)
        return serializer.data


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