from typing import Any, Optional
from django.db import models
from ckeditor.fields import RichTextField
import os
from django.utils import timezone



# Create your models here.



def author_image_path(instance, filename):
    """
    Returns a string representing the path where the image file should be saved for an Author instance.

    Args:
        instance: An instance of the Author model.
        filename: A string representing the original filename of the image file.

    Returns:
        A string representing the path where the image file should be saved.
    """
    # Get the file extension from the original filename
    file_extension = filename.split('.')[-1]
    # Use the author's id as the new filename
    name = instance.id
    return f'authors/images/{name}.{file_extension}' 

class Author(models.Model):
    """
    Represents an author in the system.

    Fields:
        id: An auto-incrementing integer field that serves as the primary key for the model.
        name: A character field that stores the author's first name.
        surname: A character field that stores the author's last name.
        company_name: A character field that stores the name of the author's company.
        email: An email field that stores the author's email address.
        image: An image field that stores the author's profile picture. The `upload_to` argument specifies the path where the image file should be saved, and the `default` argument specifies the default image to use if no image is provided.

    Methods:
        __str__: Returns a string representation of the author, which is the concatenation of the author's first and last name.
        save: Overrides the default `save` method to update the image path with the author's id if the image name is None.
        delete: Overrides the default `delete` method to delete the image file associated with the author instance.
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to=author_image_path, default= 'authors/images/default.png', blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the author, which is the concatenation of the author's first and last name.
        """
        return self.name + ' ' + self.surname
    
    def save(self, *args, **kwargs):
        """
        Overrides the default `save` method to update the image path with the author's id if the image name is None.
        """
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
        """
        Overrides the default `delete` method to delete the image file associated with the Author instance.
        """
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
    