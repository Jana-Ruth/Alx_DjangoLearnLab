from rest_framework import generics, permissions, mixins
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly


# List all books
class ListView(generics.ListAPIView):
    """
    GET: List all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve a single book
class DetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a book
class CreateView(generics.CreateAPIView):
    """
    POST: Create a new book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Update a book
class UpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update book details (only owner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# Delete a book
class DeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book (only owner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
