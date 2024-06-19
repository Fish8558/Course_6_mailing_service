from django.contrib import admin
from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'count_views', 'is_published', 'owner',)
    list_filter = ('is_published', 'owner',)
    search_fields = ('title',)
