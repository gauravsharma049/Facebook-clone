from django.contrib import admin
from FacebookApp.models import Post, UserProfile, Like, FollowerCount
# Register your models here.
admin.site.register((Post, UserProfile, Like, FollowerCount))