# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'excerpt', 'date_posted', 'author', 'author_name']

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username

    def get_excerpt(self, obj):
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_posted'] = instance.date_posted.strftime('%d-%m-%Y %H:%M:%S')
        return representation

    def validate_title(self, value):
        """Walidacja pojedynczego pola."""
        if len(value) < 5:
            raise serializers.ValidationError(
                'Tytuł musi mieć co najmniej 5 znaków'
            )
        return value

    def validate(self, data):
        """Walidacja wielu pól naraz."""
        if data.get('title') and data.get('content'):
            if data['title'].lower() == data['content'].lower():
                raise serializers.ValidationError(
                    'Treść artykułu nie może być identyczna z tytułem'
                )
        return data
