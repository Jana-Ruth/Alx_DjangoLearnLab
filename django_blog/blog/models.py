from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Post  # if Post is defined in same file, remove this import
from taggit.managers import TaggableManager

class Profile(models.Model):
    """
    Profile extends the built-in User model with optional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensure a Profile is created for every new User, and saved on User.save().
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Tag(models.Model):
    """Simple Tag model."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Blog post model.
    - title: short title
    - content: body of the post
    - published_date: auto set when created
    - author: FK to User
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # After create/update, reverse to detail view
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    """
    Comment on a Post.
    - post: the post this comment belongs to
    - author: the user who wrote the comment
    - content: the comment body
    - created_at, updated_at: timestamps
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    def get_absolute_url(self):
        # After edit/delete, redirect to the post detail
        return reverse('post-detail', kwargs={'pk': self.post.pk})    