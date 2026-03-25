from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Activity
from books.models import Review, ReadingList
from accounts.models import Follow

@receiver(post_save, sender=Review)
def create_review_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.user,
            activity_type='review',
            target=instance,
            metadata={
                'book_title': instance.book.title,
                'rating': instance.rating
            }
        )
        print(f"✅ Created review activity for {instance.user.username}")

@receiver(post_save, sender=ReadingList)
def create_reading_list_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.user,
            activity_type='reading_list',
            target=instance,
            metadata={
                'book_title': instance.book.title,
                'status': instance.status
            }
        )
        print(f"✅ Created reading list activity for {instance.user.username}")

@receiver(post_save, sender=Follow)
def create_follow_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.follower,
            activity_type='follow',
            target=instance.followed,
            metadata={
                'followed_username': instance.followed.username
            }
        )
        print(f"✅ Created follow activity for {instance.follower.username}")