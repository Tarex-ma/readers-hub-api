from collections import Counter
from django.db.models import Q, Count, Avg
from ..models import Book, Review, ReadingList

class RecommendationService:
    """Generate book recommendations based on user history"""
    
    @staticmethod
    def get_recommendations_for_user(user, limit=10):
        """Main recommendation engine"""
        
        # Get user's reading history
        read_books = ReadingList.objects.filter(
            user=user, 
            status='read'
        ).values_list('book_id', flat=True)
        
        # Get user's highly rated books (4-5 stars)
        highly_rated = Review.objects.filter(
            user=user,
            rating__gte=4
        ).values_list('book_id', flat=True)
        
        # If no history, return popular books
        if not read_books and not highly_rated:
            return RecommendationService._get_popular_books(limit)
        
        recommendations = []
        
        # 1. Recommendations based on favorite genres
        if user.favorite_genres:
            genre_recs = RecommendationService._recommend_by_genres(
                user, read_books, limit//3
            )
            recommendations.extend(genre_recs)
        
        # 2. Recommendations based on highly rated books
        if highly_rated:
            similar_recs = RecommendationService._recommend_similar_books(
                highly_rated, read_books, limit//3
            )
            recommendations.extend(similar_recs)
        
        # 3. Recommendations from followed users
        following_recs = RecommendationService._recommend_from_following(
            user, read_books, limit//3
        )
        recommendations.extend(following_recs)
        
        # 4. Fill remaining with popular books
        remaining = limit - len(recommendations)
        if remaining > 0:
            popular = RecommendationService._get_popular_books(
                remaining, exclude_ids=read_books
            )
            recommendations.extend(popular)
        
        # Remove duplicates and return
        seen = set()
        unique_recs = []
        for book in recommendations:
            if book.id not in seen:
                seen.add(book.id)
                unique_recs.append(book)
        
        return unique_recs[:limit]
    
    @staticmethod
    def _recommend_by_genres(user, exclude_ids, limit):
        """Recommend books from user's favorite genres"""
        return Book.objects.filter(
            genre__in=user.favorite_genres
        ).exclude(
            id__in=exclude_ids
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating', '-total_reviews')[:limit]
    
    @staticmethod
    def _recommend_similar_books(book_ids, exclude_ids, limit):
        """Find books similar to highly rated ones"""
        # Get genres of highly rated books
        genres = Book.objects.filter(id__in=book_ids).values_list('genre', flat=True)
        genre_counter = Counter(genres)
        top_genres = [g for g, _ in genre_counter.most_common(3)]
        
        # Get authors of highly rated books
        authors = Book.objects.filter(id__in=book_ids).values_list('author', flat=True)
        author_counter = Counter(authors)
        top_authors = [a for a, _ in author_counter.most_common(3)]
        
        # Find similar books
        return Book.objects.filter(
            Q(genre__in=top_genres) | Q(author__in=top_authors)
        ).exclude(
            id__in=exclude_ids
        ).exclude(
            id__in=book_ids
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')[:limit]
    
    @staticmethod
    def _recommend_from_following(user, exclude_ids, limit):
        """Recommend books that followed users enjoyed"""
        following_users = user.following.values_list('followed', flat=True)
        
        # Get highly rated books from followed users
        return Book.objects.filter(
            reviews__user__in=following_users,
            reviews__rating__gte=4
        ).exclude(
            id__in=exclude_ids
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            follower_count=Count('reviews__user', distinct=True)
        ).order_by('-follower_count', '-avg_rating')[:limit]
    
    @staticmethod
    def _get_popular_books(limit, exclude_ids=None):
        """Get most popular books overall"""
        queryset = Book.objects.all()
        if exclude_ids:
            queryset = queryset.exclude(id__in=exclude_ids)
        
        return queryset.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-total_reviews', '-avg_rating')[:limit]