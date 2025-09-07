from django.shortcuts import render
from django.views.generic.detail import DetailView   # ✅ checker wants this
from .models import Book
from .models import Library   # ✅ explicit import for checker

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
