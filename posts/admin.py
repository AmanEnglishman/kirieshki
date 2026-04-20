from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_published',
        'is_pinned',
        'views_count',
        'created_at',
        'updated_at',
        'likes_count',
        'comments_count',
    )
    list_filter = ('category', 'is_published', 'is_pinned', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
