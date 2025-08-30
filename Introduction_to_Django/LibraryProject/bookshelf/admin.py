from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these fields in the list view
    list_filter = ('publication_year', 'author')  # Add filters for sidebar
    search_fields = ('title', 'author')  # Enable search by title/author

# Register with customization
admin.site.register(Book, BookAdmin)
