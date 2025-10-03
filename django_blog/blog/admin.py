from django.contrib import admin

from .models import Profile, Post

admin.site.register(Profile)
# Register your models here.

admin.site.register(Post)