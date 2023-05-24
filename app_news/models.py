from django.db import models
from ckeditor.fields import RichTextField
import os


# Create your models here.

#TODO: Create Autohor model With fields: name, surname, age, email, phone, description
#TODO: Posts model with fields: title, description, created_at, updated_at, author(FK)
#TODO: Create Database for users login and register

def author_image_path(instance, filename):
    # Get the file extension from the original filename
    file_extension = filename.split('.')[-1]
    # Use the author's id as the new filename
    name = instance.id
    return f'authors/images/{name}.{file_extension}' 

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to=author_image_path, default= 'authors/images/default.png', blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.surname
    
    def save(self, *args, **kwargs):
        # Save the instance to get the id assigned
        super().save(*args, **kwargs)

        # Check if the instance has an image and if the image name is None
        if self.image and self.image.name == 'authors/images/None.' + self.image.name.split('.')[-1]:
            # Update the image name with the correct id
            image_name = self.image.name
            file_extension = image_name.split('.')[-1]
            new_image_path = f'authors/images/{self.id}.{file_extension}'

            # Save the instance with the updated image path
            os.rename(self.image.path, os.path.join(os.path.dirname(self.image.path), f'{self.id}.{file_extension}'))
            self.image.name = new_image_path
            super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the image file associated with the Author instance
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    
    

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField()
    tags = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='posts/images/', default='posts/images/default.png')
    excerpt = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    last_login = models.DateTimeField()
    profile_image = models.ImageField(upload_to='users/images/', default='users/images/default.png')
    bio = models.TextField()

    def __str__(self):
        return self.username
