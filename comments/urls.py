from django.urls import path
from . import views

urlpatterns = [
    path('reviews/<int:review_id>/comments/', 
         views.CommentListCreateView.as_view(), 
         name='comment-list'),
    path('comments/<int:pk>/', 
         views.CommentDetailView.as_view(), 
         name='comment-detail'),
]