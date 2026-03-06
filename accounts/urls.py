from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profiles
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]

# Add to accounts/urls.py

urlpatterns += [
    # Follow system
    path('users/<int:user_id>/follow/', views.FollowView.as_view(), name='follow-user'),
    path('users/<int:user_id>/followers/', views.FollowersListView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', views.FollowingListView.as_view(), name='user-following'),
    
    # User stats
    path('users/<int:pk>/stats/', views.UserDetailView.as_view(), name='user-stats'),
    path('profile/avatar/', views.AvatarUploadView.as_view(), name='avatar-upload'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('request-verification/', 
         views.RequestVerificationEmailView.as_view(), 
         name='request-verification'),

]