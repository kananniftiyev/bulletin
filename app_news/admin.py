from django.contrib import admin
from . models import Author, Posts, User

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted','tags')
    list_filter = ('author', 'date_posted','tags')
    search_fields = ('title', 'content','tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_posted'

admin.site.register(Author)
admin.site.register(Posts)
admin.site.register(User)