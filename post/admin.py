from django.contrib import admin
from .models import Post, Following, Like

# Register your models here.

admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Like)