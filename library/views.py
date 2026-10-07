from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer
from .services import AuthorService, GenreService, BookService


class SoftDeleteViewSetMixin:
    """
    Миксин для ViewSet: использует сервисный слой
    для получения данных и мягкого удаления.
    """
    service = None  # переопределяется в наследниках

    def get_queryset(self):
        """Список — только неудалённые объекты."""
        return self.service.get_active()

    def destroy(self, request, *args, **kwargs):
        """DELETE — мягкое удаление через сервис."""
        instance = self.get_object()
        self.service.soft_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    service = AuthorService


class GenreViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    service = GenreService


class BookViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    service = BookService