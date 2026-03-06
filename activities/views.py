from rest_framework import generics, permissions
from django.db.models import Q
from .models import Activity
from .serializers import ActivitySerializer

class FeedView(generics.ListAPIView):
    """Get activity feed from users you follow"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.values_list('followed', flat=True)
        
        # Get activities from followed users + own activities
        return Activity.objects.filter(
            Q(user__in=following_users) | Q(user=self.request.user)
        ).select_related('user').prefetch_related(
            'content_type'
        )[:50]  # Limit to 50 most recent activities

class UserActivitiesView(generics.ListAPIView):
    """Get activities for a specific user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Activity.objects.filter(user_id=user_id)[:30]
