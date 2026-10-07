---

# Лабораторная работа №2
## REST API для библиотеки книг

### Описание
REST API для управления библиотекой: авторы, жанры, книги.
Построен на Django REST Framework + PostgreSQL 16.

### Стек
- Python 3.12+
- Django 6.x
- Django REST Framework 3.18+
- PostgreSQL 16
- Docker Compose

### Запуск
```bash
docker compose up --build -d
docker compose exec app python manage.py migrate

Приложение доступно на http://127.0.0.1:8000/.