from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from posts.validators import (
    validate_author_age,
    validate_email,
    validate_password,
    validate_title,
)


# Пользователь
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["birth_date"]

    def clean(self):
        super().clean()
        validate_email(self.email)

    def set_password(self, raw_password):
        super().set_password(raw_password)
        validate_password(raw_password)
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# Пост
class Post(models.Model):
    title = models.CharField(max_length=255, validators=[validate_title])
    content = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def clean(self):
        if self.author:
            validate_author_age(self.author.birth_date)
        else:
            raise ValidationError("Пользователь не найден")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


# Комментарий
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]
