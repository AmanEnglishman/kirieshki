from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'ip_address', 'visitor_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'ip_address', 'visitor_id')
    readonly_fields = ('created_at',)
