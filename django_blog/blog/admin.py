from django.contrib import admin

from .models import Profile, Post, Comment

admin.site.register(Profile)
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
