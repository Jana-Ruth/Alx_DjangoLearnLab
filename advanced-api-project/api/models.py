from django.db import models

class Author(models.Model):
    """
    Represents an author who can have multiple books.
    Fields:
        - name: The author's full name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an author.
    Fields:
        - title: The title of the book.
        - publication_year: The year the book was published.
        - author: A ForeignKey to Author (one-to-many relationship).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
