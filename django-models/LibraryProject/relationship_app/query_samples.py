# LibraryProject/relationship_app/query_samples.py

import os
import django

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def run_queries():
    # 1. Query all books by a specific author
    author_name = "Chinua Achebe"
    books_by_author = Book.objects.filter(author__name=author_name)
    print(f"\nBooks by {author_name}:")
    for book in books_by_author:
        print("-", book.title)

    # 2. List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books_in_library:
            print("-", book.title)
    except Library.DoesNotExist:
        print(f"\nNo library found with name {library_name}")

    # 3. Retrieve the librarian for a library
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian of {library.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"\nNo librarian assigned to {library.name}")


if __name__ == "__main__":
    run_queries()
