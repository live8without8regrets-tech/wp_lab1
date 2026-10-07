import uuid
from django.db import models


class Author(models.Model):
    """Автор книги."""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, verbose_name="Имя")
    birth_year = models.IntegerField(null=True, blank=True, verbose_name="Год рождения")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр книги."""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга."""
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('issued', 'Выдана'),
        ('archived', 'В архиве'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name="Автор",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name="Жанр",
    )
    year = models.IntegerField(verbose_name="Год издания")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="Статус",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.title} ({self.year})"