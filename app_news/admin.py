from django.contrib import admin
from . models import TopPosts


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('author', 'date')
    search_fields = ('title',)
    date_hierarchy = 'date'


admin.site.register(TopPosts, PostAdmin)
