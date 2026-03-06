from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('users/<int:user_id>/activities/', views.UserActivitiesView.as_view(), name='user-activities'),
]