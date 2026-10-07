from rest_framework import serializers
from .models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'birth_year', 'country',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id', 'name', 'description',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']


class BookSerializer(serializers.ModelSerializer):
    # Удобно возвращать название автора и жанра в ответе
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_name',
            'genre', 'genre_name', 'year', 'status',
            'description',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

    def validate_year(self, value):
        """Год не может быть больше текущего."""
        from datetime import date
        if value > date.today().year:
            raise serializers.ValidationError(
                "Год издания не может быть больше текущего."
            )
        if value < 0:
            raise serializers.ValidationError("Год не может быть отрицательным.")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название не может быть пустым.")
        return value.strip()