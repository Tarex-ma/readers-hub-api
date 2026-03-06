from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('sci_fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('self_help', 'Self Help'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    description = models.TextField()
    page_count = models.IntegerField(null=True, blank=True)
    
    # Stats (will be updated when reviews are added)
    average_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def update_rating(self):
        """Update average rating based on all reviews"""
        from .models import Review  # Import here to avoid circular import
        reviews = self.reviews.all()
        if reviews:
            self.average_rating = sum(r.rating for r in reviews) / len(reviews)
            self.total_reviews = len(reviews)
        else:
            self.average_rating = 0
            self.total_reviews = 0
        self.save()


        # Add to books/models.py - after the Book model

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField()
    date_read = models.DateField()
    spoiler = models.BooleanField(default=False)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Likes (many-to-many relationship)
    likes = models.ManyToManyField(
        'accounts.CustomUser',
        related_name='liked_reviews',
        blank=True
    )
    
    class Meta:
        # Ensure one review per user per book
        unique_together = ['user', 'book']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the book's average rating
        self.book.update_rating()


class ReadingList(models.Model):
    STATUS_CHOICES = [
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('read', 'Read'),
        ('did_not_finish', 'Did Not Finish'),
    ]
    
    user = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.CASCADE, 
        related_name='reading_list'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reading_list_entries'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_read')
    
    # Optional fields for tracking reading progress
    current_page = models.IntegerField(default=0, null=True, blank=True)
    started_at = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)
    
    # Notes about the reading experience
    personal_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ensure one entry per user per book
        unique_together = ['user', 'book']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"
    
    @property
    def reading_progress(self):
        if self.book.page_count and self.current_page:
            return int((self.current_page / self.book.page_count) * 100)
        return 0