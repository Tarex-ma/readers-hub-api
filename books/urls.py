from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    path('', views.BookListView.as_view(), name='book-list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Nested review endpoints
    path('<int:book_id>/reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('<int:book_id>/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Standalone review endpoints
    path('reviews/<int:pk>/like/', views.like_review, name='review-like'),
    
    # User's reviews
    path('users/<int:user_id>/reviews/', views.UserReviewListView.as_view(), name='user-reviews'),

    # Reading list endpoints
    path('my-reading-list/', views.ReadingListView.as_view(), name='my-reading-list'),
    path('my-reading-list/<int:pk>/', views.ReadingListDetailView.as_view(), name='my-reading-list-detail'),
    path('users/<int:user_id>/reading-list/', views.UserReadingListView.as_view(), name='user-reading-list'),
    
    # Book cover upload
    path('<int:pk>/upload-cover/', views.BookCoverUploadView.as_view(), name='book-cover-upload'),

    # Recommendations
    path('recommendations/', views.RecommendationsView.as_view(), name='recommendations'),
]