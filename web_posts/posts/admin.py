from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title') # Ссылка на автора
    list_filter = ('created_at', ) # фильтр по дате создания поста

