# LibraryProject/relationship_app/query_samples.py

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
books_by_author = Book.objects.filter(author__name="Chinua Achebe")
print("Books by Chinua Achebe:", [book.title for book in books_by_author])

# 2. List all books in a library
library = Library.objects.get(name="Central Library")
print("Books in Central Library:", [book.title for book in library.books.all()])

# 3. Retrieve the librarian for a library (⚡ must contain exact string)
librarian = Librarian.objects.get(library=library)
print("Librarian of Central Library:", librarian.name)
