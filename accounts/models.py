from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
     # Add custom fields
    bio= models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/',null=True,blank=True)
    favorite_genre = models.JSONField(default=list, blank=True)
    reading_goal = models.JSONField(default=list, blank=True)
    email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
    
    @property
    def books_read_count(self):
        # This will be implemented later when we add reading lists
     return 0
    

# Add this to accounts/models.py - after CustomUser class
class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='following'  # Users this person follows
    )
    followed = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='followers'  # Users following this person
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'followed']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

# Also add helper methods to CustomUser model
# In accounts/models.py, inside the CustomUser class, add:

@property
def followers_count(self):
    return self.followers.count()

@property
def following_count(self):
    return self.following.count()

def follow(self, user):
    """Follow another user"""
    return Follow.objects.get_or_create(follower=self, followed=user)

def unfollow(self, user):
    """Unfollow another user"""
    Follow.objects.filter(follower=self, followed=user).delete()

def is_following(self, user):
    """Check if following another user"""
    return self.following.filter(followed=user).exists()