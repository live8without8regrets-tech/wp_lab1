from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, BookViewSet


router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = router.urls