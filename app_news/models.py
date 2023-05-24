from django.db import models

# Create your models here.

#TODO: Create Autohor model With fields: name, surname, age, email, phone, description
#TODO: Posts model with fields: title, description, created_at, updated_at, author(FK)
#TODO: Create Database for users login and register

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField()
    tags = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='posts/images/')
    excerpt = models.TextField()
    date = models.DateField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    last_login = models.DateTimeField()
    profile_image = models.ImageField(upload_to='users/images/')
    bio = models.TextField()
