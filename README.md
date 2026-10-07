# Лабораторная работа №1
## Знакомство с клиент-серверным взаимодействием

### Описание
Веб-сервер на Django, отдающий JSON с количеством дней до Нового года.

### Стек
- Python 3.12+
- Django 6.x
- Docker

### Запуск через Docker
```bash
docker build -t wp_lab1 .
docker run -p 8000:8000 wp_lab1
```

### Проверка
```bash
curl.exe http://127.0.0.1:8000/info
```

Пример ответа:
```json
{"days_before_new_year": 86}
```

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
```

Приложение доступно на `http://127.0.0.1:8000/`.

### Основные URL
| URL | Описание |
|---|---|
| `/admin/` | Админка |
| `/info` | Лаба №1: дни до Нового года |
| `/api/` | Корень API |
| `/api/authors/` | Авторы |
| `/api/genres/` | Жанры |
| `/api/books/` | Книги |

### Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/books/` | Список книг (пагинация) |
| GET | `/api/books/{id}/` | Книга по ID |
| POST | `/api/books/` | Создать книгу |
| PUT | `/api/books/{id}/` | Полное обновление |
| PATCH | `/api/books/{id}/` | Частичное обновление |
| DELETE | `/api/books/{id}/` | Soft delete |

Аналогично для `/api/authors/` и `/api/genres/`.

### Пагинация
Параметр `?page=N` (по умолчанию 10 записей на страницу).
Ответ содержит `count`, `next`, `previous`, `results`.

### Soft Delete
`DELETE` не удаляет запись физически — устанавливает `deleted_at`.
Удалённые записи не возвращаются через API, но доступны в админке
(`/admin/library/book/` → фильтр `By deleted_at`).

### Валидация
- Год издания ≤ текущего года.
- Название не пустое.
- Статус из списка: `available`, `issued`, `archived`.

### Админка
`http://127.0.0.1:8000/admin/`

Суперпользователь:
```bash
docker compose exec app python manage.py createsuperuser
```

### Примеры запросов

```bash
# Лаба №1
curl.exe http://127.0.0.1:8000/info

# Список книг
curl.exe "http://127.0.0.1:8000/api/books/?page=1"

# Soft delete
curl.exe -X DELETE http://127.0.0.1:8000/api/books/1/
```