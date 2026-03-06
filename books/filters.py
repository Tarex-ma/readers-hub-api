import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='lte')
    published_after = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    published_before = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    genre = django_filters.CharFilter(lookup_expr='iexact')
    author = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['genre', 'author', 'min_rating', 'max_rating', 
                 'published_after', 'published_before']