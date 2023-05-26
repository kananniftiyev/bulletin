from django.contrib import admin
from . models import Author, Posts


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date','tags')
    list_filter = ('author', 'date','tags')
    search_fields = ('title', 'content','tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email')
    search_fields = ('name', 'surname', 'email')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Posts, PostAdmin)
