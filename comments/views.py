from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer
from books.models import Review

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(
            review_id=review_id,
            parent__isnull=True  # Only top-level comments
        ).select_related('user')
    
    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(user=self.request.user, review=review)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        # Allow DELETE/UPDATE only for comment owner or admin
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user == request.user or request.user.is_staff
        return True
