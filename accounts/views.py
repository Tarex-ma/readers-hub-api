from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status,settings
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserListSerializer,FollowSerializer,AvatarUploadSerializer,UserDetailWithStatsSerializer
from .models import Follow,CustomUser
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .utils.email_utils import send_verification_email, send_welcome_email
import jwt

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.AllowAny,)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.AllowAny,)

class FollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """Follow a user"""
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow, created = request.user.follow(user_to_follow)
        
        if created:
            # Create activity
            from activities.models import Activity
            from django.contrib.contenttypes.models import ContentType
            Activity.objects.create(
                user=request.user,
                activity_type='follow',
                target=user_to_follow,
                metadata={'followed_username': user_to_follow.username}
            )
            return Response({'message': f'Now following {user_to_follow.username}'})
        else:
            return Response(
                {'error': 'Already following this user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, user_id):
        """Unfollow a user"""
        user_to_unfollow = get_object_or_404(User, id=user_id)
        request.user.unfollow(user_to_unfollow)
        return Response(
            {'message': f'Unfollowed {user_to_unfollow.username}'},
            status=status.HTTP_204_NO_CONTENT
        )

class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FollowSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(followed_id=user_id).select_related('follower')

class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FollowSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(follower_id=user_id).select_related('followed')


class AvatarUploadView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AvatarUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user
    
class RequestVerificationEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if not user.email_verified:
            send_verification_email(user)
            return Response(
                {'message': 'Verification email sent'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Email already verified'},
            status=status.HTTP_400_BAD_REQUEST
        )

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            
            if payload.get('type') != 'email_verification':
                return Response(
                    {'error': 'Invalid token type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.get(id=payload['user_id'])
            
            if user.email_verified:
                return Response(
                    {'message': 'Email already verified'},
                    status=status.HTTP_200_OK
                )
            
            user.email_verified = True
            user.save()
            
            # Send welcome email
            send_welcome_email(user)
            
            return Response(
                {'message': 'Email verified successfully'},
                status=status.HTTP_200_OK
            )
            
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Verification link expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )