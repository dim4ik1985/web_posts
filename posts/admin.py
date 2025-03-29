from django.contrib import admin

from .models import Post, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title")  # Ссылка на автора
    list_filter = ("created_at",)  # фильтр по дате создания поста


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_superuser", "is_staff")
