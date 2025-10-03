from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(title='P', content='C', author=self.user1)

    def test_create_comment_authenticated(self):
        self.client.login(username='u2', password='pass')
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        response = self.client.post(url, {'content': 'Nice post!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.comments.filter(content='Nice post!').exists())

    def test_edit_comment_only_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user2, content='a')
        self.client.login(username='u1', password='pass')  # not the author
        url = reverse('comment-edit', kwargs={'pk': comment.pk})
        response = self.client.post(url, {'content': 'changed'}, follow=True)
        # user1 should be forbidden (UserPassesTestMixin redirects to login by default),
        # but check that comment content didn't change:
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'a')

    def test_delete_comment_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user2, content='to delete')
        self.client.login(username='u2', password='pass')
        url = reverse('comment-delete', kwargs={'pk': comment.pk})
        response = self.client.post(url, follow=True)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
