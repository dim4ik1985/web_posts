from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from posts.models import User, Post, Comment
from posts.validators import validate_password, validate_author_age, validate_title, validate_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone_number', 'birth_date')
        extra_kwargs = {'password': {'write_only': True}}

    """Проверка email: только разрешенные домены (mail.ru, yandex.ru)."""
    def validate(self, data):
        if 'email' in data:
            try:
                validate_email(data['email'])
            except ValidationError as e:
                raise serializers.ValidationError({'email': e.messages})
        return data

    """Проверка пароля: минимум 8 символов и хотя бы одна цифра."""
    def create(self, validated_data):
        try:
            validate_password(validated_data['password'])  # Проверяем пароль
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})  # Преобразуем ошибку в формат DRF

        validated_data['password'] = make_password(validated_data['password'])  # Хешируем пароль
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'image', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def validate(self, data):
        if self.context['request'].user:
            try:
                validate_author_age(self.context['request'].user.birth_date)
            except ValidationError as e:
                raise serializers.ValidationError({'author': e.messages})
        if 'title' in data:
            try:
                validate_title(data['title'])
            except ValidationError as e:
                raise serializers.ValidationError({'title': e.messages})
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created_at')
        read_only_fields = ('author', )



