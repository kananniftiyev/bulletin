from django.db import models
import os
from django.utils import timezone
from django.utils.text import slugify



# Create your models here.

class TopPosts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    #content = models.TextField(max_length=10000, null=True)
    author = models.CharField(max_length=1000)
    #slug = models.SlugField(max_length=1000)
    #category = models.CharField(max_length=100, default="No category available")
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    urlToPost = models.URLField(max_length=5000, null=True)

    def __str__(self):
        return self.title
    

class LatestPosts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    #category = models.CharField(max_length=100, default="No category available")
    urlToPost = models.URLField(max_length=5000, null=True)
    
    