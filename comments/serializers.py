from rest_framework import serializers
from .models import Comment
from accounts.serializers import UserListSerializer

class CommentSerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    
    def validate(self, data):
        # Ensure parent comment belongs to same review
        if data.get('parent'):
            if data['parent'].review != data.get('review', self.instance.review if self.instance else None):
                raise serializers.ValidationError(
                    "Parent comment must be on the same review"
                )
        return data