from django.contrib import admin
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'birth_year', 'deleted_at')
    search_fields = ('name',)
    list_filter = ('country',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year', 'status', 'deleted_at')
    list_filter = ('status', 'genre', 'deleted_at')
    search_fields = ('title', 'author__name')
    raw_id_fields = ('author',)