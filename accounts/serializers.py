from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Follow,CustomUser

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'bio', 'favorite_genre', 'reading_goal')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['email_verified'] = False  # Start unverified
        user = User.objects.create_user(**validated_data)
        
        # Send verification email
        from .utils.email_utils import send_verification_email
        send_verification_email(user)
        
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar', 'favorite_genre', 
                 'reading_goal', 'date_joined', 'books_read_count')
        read_only_fields = ('id', 'date_joined')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'bio', 'books_read_count')


# Add to accounts/serializers.py

class FollowSerializer(serializers.ModelSerializer):
    follower_details = UserListSerializer(source='follower', read_only=True)
    followed_details = UserListSerializer(source='followed', read_only=True)
    
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'followed', 'follower_details', 'followed_details', 'created_at')
        read_only_fields = ('follower', 'created_at')

class UserDetailWithStatsSerializer(UserListSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    reviews_count = serializers.SerializerMethodField()
    reading_list_stats = serializers.SerializerMethodField()
    
    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + (
            'followers_count', 'following_count', 'reviews_count', 
            'reading_list_stats', 'date_joined'
        )
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_reading_list_stats(self, obj):
        from books.models import ReadingList
        stats = {
            'want_to_read': obj.reading_list.filter(status='want_to_read').count(),
            'currently_reading': obj.reading_list.filter(status='currently_reading').count(),
            'read': obj.reading_list.filter(status='read').count(),
            'did_not_finish': obj.reading_list.filter(status='did_not_finish').count(),
        }
        return stats
    
class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']