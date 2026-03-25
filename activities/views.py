from rest_framework import generics, permissions
from django.db.models import Q
from .models import Activity
from .serializers import ActivitySerializer

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        following_users = self.request.user.following.values_list('followed_id', flat=True)

        return Activity.objects.filter(
            Q(user__in=following_users) | Q(user=self.request.user)
        ).select_related('user').order_by('-created_at')[:50]

class UserActivitiesView(generics.ListAPIView):
    """Get activities for a specific user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Activity.objects.filter(user_id=user_id)[:30]
