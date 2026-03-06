from django.contrib import admin
from .models import Book,Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_year', 'average_rating')
    list_filter = ('genre', 'publication_year')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'date_read', 'spoiler', 'created_at')
    list_filter = ('rating', 'spoiler', 'date_read')
    search_fields = ('book__title', 'user__username', 'text')
    raw_id_fields = ('user', 'book')
