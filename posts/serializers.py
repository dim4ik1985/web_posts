from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from posts.models import User, Post, Comment
from posts.validators import validate_email, validate_password, validate_author_age, validate_title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}


    # Валидация email: только разрешенные домены (mail.ru, yandex.ru)
    def validate(self, attrs):
        if 'email' in attrs:
            try:
                validate_email(attrs['email'])
            except ValidationError as e:
                raise serializers.ValidationError({'email': e.message})
        return attrs

    # Валидация password: минимум 8 символов и хотя бы одна цифра
    def create(self, validated_data):
        try:
            validate_password(validated_data['password'])  # Валидация пароля
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        validated_data['password'] = make_password(validated_data['password'])  # Хешируем пароль
        return super().create(validated_data)



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'created_at', 'updated_at', 'author']
        read_only_fields = ['author']


    def validate(self, attrs):
        if self.context['request'].user:
            try:
                validate_author_age(self.context['request'].user.birth_date) # Валидация возраста
            except ValidationError as e:
                raise serializers.ValidationError({'author': e.messages})
        if 'title' in attrs:
            try:
                validate_title(attrs['title']) # Валидация заголовка
            except ValidationError as e:
                raise serializers.ValidationError({'title': e.messages})
        return attrs

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']
