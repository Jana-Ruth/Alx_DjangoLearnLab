from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books / Create new book
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow everyone to read, but only authenticated users can create
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Retrieve / Update / Delete a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Restrict update & delete to authenticated users
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
