from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Activity
from accounts.serializers import UserListSerializer
from books.serializers import ReviewSerializer, BookListSerializer

class ActivitySerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)
    target_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = '__all__'
    
    def get_target_object(self, obj):
        # Return serialized representation of the target object
        if obj.target:
            if obj.activity_type == 'review':
                from books.serializers import ReviewSerializer
                return ReviewSerializer(obj.target).data
            elif obj.activity_type == 'reading_list':
                from books.serializers import ReadingListSerializer
                return ReadingListSerializer(obj.target).data
            elif obj.activity_type == 'follow':
                from accounts.serializers import FollowSerializer
                return FollowSerializer(obj.target).data
        return None