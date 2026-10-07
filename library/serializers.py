from datetime import date

from rest_framework import serializers

from .models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора."""

    class Meta:
        model = Author
        fields = [
            'id', 'uuid',
            'name', 'birth_year', 'country',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at', 'deleted_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя автора не может быть пустым.")
        return value.strip()

    def validate_birth_year(self, value):
        if value is None:
            return value
        current_year = date.today().year
        if value < 0:
            raise serializers.ValidationError("Год рождения не может быть отрицательным.")
        if value > current_year:
            raise serializers.ValidationError("Год рождения не может быть больше текущего.")
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = [
            'id', 'uuid',
            'name', 'description',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at', 'deleted_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название жанра не может быть пустым.")
        return value.strip()


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор книги."""

    # Дополнительные поля только для чтения — показывают имя автора и жанра
    author_name = serializers.CharField(source='author.name', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'uuid',
            'title',
            'author', 'author_name',
            'genre', 'genre_name',
            'year', 'status', 'description',
            'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at', 'deleted_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название не может быть пустым.")
        return value.strip()

    def validate_year(self, value):
        current_year = date.today().year
        if value < 0:
            raise serializers.ValidationError("Год не может быть отрицательным.")
        if value > current_year:
            raise serializers.ValidationError(
                "Год издания не может быть больше текущего."
            )
        return value

    def validate_status(self, value):
        allowed = ['available', 'issued', 'archived']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Статус должен быть одним из: {', '.join(allowed)}."
            )
        return value