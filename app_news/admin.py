from django.contrib import admin
from . models import Author, Posts, User

# Register your models here.

admin.site.register(Author)
admin.site.register(Posts)
admin.site.register(User)