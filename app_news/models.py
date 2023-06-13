from django.db import models
import os
from django.utils import timezone
import uuid

def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media/', new_filename)


# Create your models here.

class TopPosts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    #content = models.TextField(max_length=10000, null=True)
    author = models.CharField(max_length=1000)
    #slug = models.SlugField(max_length=1000)
    category = models.CharField(max_length=100, default="No category available", null=True)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000, null=True)
    date = models.DateField(default=timezone.now)
    urlToPost = models.URLField(max_length=5000, null=True)
    timeToRead = models.IntegerField(default=0, null=True)
    #AuthorImg = models.ImageField(null=True, default=None, blank=True)

    def __name__(self):
        return "TopPosts"

    def __str__(self):
        return self.title
    

class LatestPosts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000, null=True)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100, default="No category available", null=True)
    urlToPost = models.URLField(max_length=5000, null=True)
    timeToRead = models.IntegerField(default=0, null=True)

    def __name__(self):
        return "LatestPosts"

    def __str__(self):
        return self.title
    

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000, null=True)
    date = models.DateField(default=timezone.now)
    urlToPost = models.URLField(max_length=5000, null=True)
    category = models.CharField(max_length=100, default="Business", null=True)
    timeToRead = models.IntegerField(default=0, null=True)

    def __name__(self):
        return "Business"


    def __str__(self):
        return self.title
    
class Sport(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000, null=True)
    date = models.DateField(default=timezone.now)
    urlToPost = models.URLField(max_length=5000, null=True)
    category = models.CharField(default="Sport", max_length=100, null=True)
    timeToRead = models.IntegerField(default=0, null=True)


    def __str__(self):
        return self.title
    
    def __name__(self):
        return "Sport"
    
class EmailList(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=1000)
    date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    
    
    