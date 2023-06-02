from django.contrib import admin
from . models import TopPosts, LatestPosts, Business, Sport, EmailList
from django.db.models import Count


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'author_post_count',)
    list_filter = ('author', 'date',)
    search_fields = ('title',)
    date_hierarchy = 'date'

    def author_post_count(self, obj):
        return TopPosts.objects.filter(author=obj.author).count()
    author_post_count.short_description = 'Number of Posts by Author'


class GenAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date',)
    list_filter = ('author', 'date',)
    search_fields = ('title',)
    date_hierarchy = 'date'


class EmailListAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', 'active',)
    list_filter = ('date','active',)
    search_fields = ('email',)
    date_hierarchy = 'date'


admin.site.register(TopPosts, PostAdmin)
admin.site.register(LatestPosts, GenAdmin)
admin.site.register(Business, GenAdmin)
admin.site.register(Sport, GenAdmin)
admin.site.register(EmailList, EmailListAdmin)
admin.site.site_header = "News App Admin"