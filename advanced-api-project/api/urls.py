from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.ListView.as_view(), name="book-list"),                  # List all books
    path("books/<int:pk>/", views.DetailView.as_view(), name="book-detail"),     # Retrieve a single book
    path("books/create/", views.CreateView.as_view(), name="book-create"),       # Create a new book
    path("books/update/<int:pk>/", views.UpdateView.as_view(), name="book-update"),  # Update a book
    path("books/delete/<int:pk>/", views.DeleteView.as_view(), name="book-delete"),  # Delete a book
]
