"""
Сервисный слой для приложения library.

Содержит бизнес-логику, не зависящую от HTTP-контекста.
View-слой вызывает методы сервисов и возвращает результат.
"""
from django.utils import timezone

from .models import Author, Genre, Book


class BaseService:
    """Базовый сервис с общими операциями для всех моделей."""

    model = None  # переопределяется в наследниках

    @classmethod
    def get_active(cls):
        """Возвращает только неудалённые записи."""
        return cls.model.objects.filter(deleted_at__isnull=True)

    @classmethod
    def get_by_id(cls, obj_id):
        """Возвращает объект по id, если он не удалён. Иначе — None."""
        return cls.get_active().filter(pk=obj_id).first()

    @classmethod
    def soft_delete(cls, instance):
        """Мягкое удаление: ставит deleted_at."""
        instance.deleted_at = timezone.now()
        instance.save(update_fields=['deleted_at'])
        return instance

    @classmethod
    def restore(cls, instance):
        """Восстановление: очищает deleted_at."""
        instance.deleted_at = None
        instance.save(update_fields=['deleted_at'])
        return instance


class AuthorService(BaseService):
    model = Author


class GenreService(BaseService):
    model = Genre


class BookService(BaseService):
    model = Book

    @classmethod
    def filter_by_status(cls, status):
        """Возвращает активные книги с заданным статусом."""
        return cls.get_active().filter(status=status)

    @classmethod
    def filter_by_author(cls, author_id):
        """Возвращает активные книги автора."""
        return cls.get_active().filter(author_id=author_id)

    @classmethod
    def filter_by_genre(cls, genre_id):
        """Возвращает активные книги жанра."""
        return cls.get_active().filter(genre_id=genre_id)