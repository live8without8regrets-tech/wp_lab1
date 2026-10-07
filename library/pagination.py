from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Пагинация с поддержкой параметров:
    - ?page=N — номер страницы (по умолчанию 1)
    - ?limit=N — размер страницы (по умолчанию 10, максимум 100)
    """
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
    page_query_param = 'page'