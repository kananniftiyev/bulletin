from django.db import models
import os
from django.utils import timezone
from django.utils.text import slugify



# Create your models here.

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    content = models.TextField(max_length=10000, null=True)
    author = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    #tags = models.CharField(max_length=100)
    main_image = models.URLField(max_length=5000)
    excerpt = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # Generate slug based on the title
        super(Posts, self).save(*args, **kwargs)
    