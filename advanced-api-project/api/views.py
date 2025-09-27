from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly  # your custom permission

# List + Create
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: List all books
    POST: Create a new book (only for authenticated users)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Retrieve + Update + Delete
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a book by ID
    PUT/PATCH: Update book details (only for owner)
    DELETE: Delete a book (only for owner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
