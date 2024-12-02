from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Book, Review, Store
from .serializers import BookSerializer
from django.db.models import Prefetch
from django_query_optimizer import optimize_query


class BookListView(ListAPIView):
    """
    A view to list all books with optimized queries.
    """
    queryset = optimize_query(Book)  # Optimized queryset
    
    # queryset = Book.objects.select_related('author', 'publisher', 'author__profile') \
    # .prefetch_related(
    #     'reviews',
    #     'reviews__reviewer',
    #     'reviews__book',
    #     'stores',
    #     'stores__books',
    # )
    
    serializer_class = BookSerializer
    
class BookDetailView(RetrieveAPIView):
    """
    A view to retrieve a single book's details.
    """
    queryset = optimize_query(Book)
    serializer_class = BookSerializer
    
class AuthorBooksView(ListAPIView):
    """
    A view to list all books written by a specific author.
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Override get_queryset to filter books by author.
        """
        author_id = self.kwargs.get('author_id')  # Extract author_id from URL
        return optimize_query(Book).filter(author_id=author_id) # 