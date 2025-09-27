from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up initial test data before each test runs.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create an author and a book
        self.author = Author.objects.create(name='John Doe')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )

        # Endpoints
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        self.update_url = reverse('book-update', kwargs={'pk': self.book.id})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.id})

    # ---------- CRUD TESTS ----------

    def test_list_books(self):
        """
        ✅ Should return a list of books.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        """
        ✅ Should allow authenticated user to create a book.
        """
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """
        ❌ Should NOT allow unauthenticated users to create a book.
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """
        ✅ Should allow authenticated user to update a book.
        """
        self.client.login(username='testuser', password='password123')
        data = {'title': 'Updated Book', 'publication_year': 2021, 'author': self.author.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book_authenticated(self):
        """
        ✅ Should allow authenticated user to delete a book.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # ---------- FILTER, SEARCH, ORDER TESTS ----------

    def test_filter_books_by_year(self):
        """
        ✅ Should filter books by publication_year.
        """
        response = self.client.get(f"{self.list_url}?publication_year=2020")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_search_books_by_title(self):
        """
        ✅ Should search books by title.
        """
        response = self.client.get(f"{self.list_url}?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_order_books_by_year(self):
        """
        ✅ Should order books by publication_year.
        """
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('publication_year', response.data[0])
