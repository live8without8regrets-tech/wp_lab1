# Web Programming Labs — Django + PostgreSQL + Docker

Учебный проект по курсу **«Веб-программирование и мобильные приложения»**.

Репозиторий содержит две последовательные лабораторные работы, объединённые в одно приложение:

| # | Работа | Стек |
|---|---|---|
| 1 | Основы клиент-серверного взаимодействия | Django + Docker |
| 2 | REST API для библиотеки книг | Django REST Framework + PostgreSQL + Docker Compose |

---

# Содержание

- [Общее описание](#общее-описание)
- [Технологический стек](#технологический-стек)
- [Архитектура проекта](#архитектура-проекта)
- [Быстрый старт](#быстрый-старт)
- [Лабораторная работа №1](#лабораторная-работа-1)
- [Лабораторная работа №2](#лабораторная-работа-2)
- [API Reference](#api-reference)
- [Тестирование](#тестирование)
- [Контрольные вопросы](#контрольные-вопросы)
- [Автор](#автор)

---

## Общее описание

Проект демонстрирует полный цикл разработки веб-приложения: от простого HTTP-сервера до REST API с реляционной базой данных, мягким удалением, пагинацией, валидацией и контейнеризацией.

**Ключевые особенности:**
- Два независимых приложения в одном Django-проекте.
- Переход от SQLite к PostgreSQL через миграции.
- Разделение на слои: модели, сериализаторы, сервисы, контроллеры.
- Промышленные практики: `.env`, Docker Compose, healthcheck, soft delete.
- Готовность к масштабированию и использованию в качестве основы для дипломного проекта.

---

## Технологический стек

| Компонент | Версия | Назначение |
|---|---|---|
| Python | 3.12+ | Язык разработки |
| Django | 6.x | Веб-фреймворк |
| Django REST Framework | 3.18+ | REST API |
| PostgreSQL | 16 | Реляционная СУБД |
| psycopg2-binary | 2.9+ | Драйвер PostgreSQL |
| python-dotenv | — | Загрузка переменных окружения |
| Docker | 24+ | Контейнеризация |
| Docker Compose | v2 | Оркестрация сервисов |

---

## Архитектура проекта

```
.
├── config/                    # Конфигурация Django-проекта
│   ├── settings.py            # Настройки (БД, приложения, DRF)
│   ├── urls.py                # Корневая маршрутизация
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                      # Лаба №1: простой HTTP-сервер
│   ├── views.py               # Обработчик /info
│   ├── urls.py
│   └── apps.py
│
├── library/                   # Лаба №2: REST API библиотеки
│   ├── migrations/            # Миграции БД
│   │   ├── 0001_initial.py
│   │   └── 0002_author_uuid_book_uuid_genre_uuid.py
│   ├── models.py              # Author, Genre, Book
│   ├── serializers.py         # DTO + валидация
│   ├── services.py            # Бизнес-логика
│   ├── views.py               # ViewSet'ы (HTTP-слой)
│   ├── pagination.py          # Кастомная пагинация
│   ├── urls.py                # Router для API
│   └── admin.py               # Регистрация в админке
│
├── Dockerfile                 # Образ приложения
├── docker-compose.yml         # App + PostgreSQL
├── requirements.txt
├── .env.example               # Шаблон переменных окружения
├── .dockerignore
├── .gitignore
├── manage.py
└── README.md
```

### Разделение ответственности

| Слой | Файл | Ответственность |
|---|---|---|
| **Модель** | `models.py` | Структура данных, ORM, поля |
| **DTO** | `serializers.py` | Формат JSON, валидация входных данных |
| **Сервис** | `services.py` | Бизнес-логика, не зависит от HTTP |
| **Контроллер** | `views.py` | Приём HTTP, вызов сервиса, ответ |
| **Пагинация** | `pagination.py` | Управление размером страницы |
| **Маршрутизация** | `urls.py` | Соответствие URL ↔ ViewSet |

Такая структура упрощает тестирование, поддержку и развитие проекта.

---

## Быстрый старт

### Требования

- Docker Desktop
- Docker Compose v2
- Git

### Запуск

```bash
# 1. Клонировать репозиторий
git clone https://github.com/live8without8regrets-tech/wp_lab1.git
cd wp_lab1

# 2. Создать .env из шаблона
copy .env.example .env

# 3. Запустить контейнеры
docker compose up --build -d

# 4. Дождаться старта PostgreSQL (15 секунд)
timeout /t 15

# 5. Применить миграции
docker compose exec app python manage.py migrate

# 6. (Опционально) Создать суперпользователя
docker compose exec app python manage.py createsuperuser
```

Приложение доступно:

- **API Root:** http://127.0.0.1:8000/api/
- **Админка:** http://127.0.0.1:8000/admin/
- **Лаба №1:** http://127.0.0.1:8000/info

### Остановка

```bash
docker compose down           # остановить контейнеры
docker compose down -v        # остановить + удалить БД
```

---

## Лабораторная работа №1

### Тема
**Знакомство с клиент-серверным взаимодействием**

### Цель
Изучение основ клиент-серверной архитектуры, освоение HTTP-протокола, получение практических навыков создания веб-сервера и обработки запросов.

### Реализация

**Обработчик `/info`** возвращает JSON с количеством дней до Нового года.

**Файл:** `core/views.py`

```python
from django.http import JsonResponse
from datetime import date


def info_view(request):
    today = date.today()
    new_year = date(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    return JsonResponse({"days_before_new_year": days_left})
```

### Проверка

```bash
curl.exe http://127.0.0.1:8000/info
```

**Ответ:**

```json
{"days_before_new_year": 86}
```

### Критерии приёмки

| Критерий | Статус |
|---|---|
| Репозиторий на GitHub | ✅ |
| README с инструкциями | ✅ |
| Рабочий эндпоинт `/info` | ✅ |
| Корректный расчёт дней до Нового года | ✅ |
| Контейнеризация через Docker | ✅ |

---

## Лабораторная работа №2

### Тема
**Проектирование и реализация RESTful API**

### Цель
Разработка REST API с реляционной БД, освоение ORM, миграций, soft delete, пагинации, валидации, контейнеризации.

### Предметная область
Управление библиотекой книг. Три сущности:
- **Author** — автор книги.
- **Genre** — жанр книги.
- **Book** — книга.

### Модели

**Author:**

| Поле | Тип | Описание |
|---|---|---|
| `id` | BigAutoField | PK, автоинкремент |
| `uuid` | UUIDField | Уникальный идентификатор |
| `name` | CharField | Имя автора |
| `birth_year` | IntegerField | Год рождения |
| `country` | CharField | Страна |
| `created_at` | DateTimeField | Создано (auto) |
| `updated_at` | DateTimeField | Обновлено (auto) |
| `deleted_at` | DateTimeField | Мягкое удаление |

**Genre:**

| Поле | Тип | Описание |
|---|---|---|
| `id` | BigAutoField | PK |
| `uuid` | UUIDField | Уникальный идентификатор |
| `name` | CharField | Название (unique) |
| `description` | TextField | Описание |
| `created_at`, `updated_at`, `deleted_at` | DateTime | Временные метки |

**Book:**

| Поле | Тип | Описание |
|---|---|---|
| `id` | BigAutoField | PK |
| `uuid` | UUIDField | Уникальный идентификатор |
| `title` | CharField | Название |
| `author` | ForeignKey | Ссылка на Author |
| `genre` | ForeignKey | Ссылка на Genre |
| `year` | IntegerField | Год издания |
| `status` | CharField | `available` / `issued` / `archived` |
| `description` | TextField | Описание |
| `created_at`, `updated_at`, `deleted_at` | DateTime | Временные метки |

### Миграции

Все изменения схемы выполняются через миграции.

```bash
# Применить все миграции
docker compose exec app python manage.py migrate

# Создать новую миграцию (после правки models.py)
docker compose exec app python manage.py makemigrations library

# Проверить статус
docker compose exec app python manage.py showmigrations library
```

**Миграции в репозитории:**

```
library/migrations/
├── 0001_initial.py                          # Начальная схема
└── 0002_author_uuid_book_uuid_genre_uuid.py # Добавление UUID
```

### Мягкое удаление (Soft Delete)

Физическое удаление записей из БД запрещено. Вместо `DELETE` устанавливается поле `deleted_at`.

**Логика:**

- `GET /api/books/` возвращает только записи с `deleted_at IS NULL`.
- `DELETE /api/books/{id}/` устанавливает `deleted_at = now()`.
- `GET /api/books/{id}/` для удалённой записи возвращает 404.
- Восстановление возможно через админку (очистить `deleted_at`).

**Реализация:** `library/services.py`

```python
@classmethod
def soft_delete(cls, instance):
    instance.deleted_at = timezone.now()
    instance.save(update_fields=['deleted_at'])
    return instance
```

### Пагинация

Кастомный класс в `library/pagination.py`:

```python
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
    page_query_param = 'page'
```

**Параметры:**

| Параметр | По умолчанию | Максимум | Описание |
|---|---|---|---|
| `page` | 1 | — | Номер страницы |
| `limit` | 10 | 100 | Размер страницы |

**Формат ответа:**

```json
{
    "count": 13,
    "next": "http://127.0.0.1:8000/api/books/?limit=5&page=2",
    "previous": null,
    "results": [ ... ]
}
```

### Валидация

Валидация выполняется на уровне сериализаторов (`library/serializers.py`).

| Поле | Правило |
|---|---|
| `title` | Не пустое |
| `year` | Не больше текущего года, неотрицательное |
| `status` | Одно из: `available`, `issued`, `archived` |
| `name` (автор, жанр) | Не пустое |

**Пример ошибки:**

```json
{"year": ["Год издания не может быть больше текущего."]}
```

---

## API Reference

Базовый префикс: `/api/`

### Authors

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/authors/` | Список авторов (пагинация) |
| GET | `/api/authors/{id}/` | Автор по ID |
| POST | `/api/authors/` | Создать автора |
| PUT | `/api/authors/{id}/` | Полное обновление |
| PATCH | `/api/authors/{id}/` | Частичное обновление |
| DELETE | `/api/authors/{id}/` | Soft delete |

### Genres

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/genres/` | Список жанров |
| GET | `/api/genres/{id}/` | Жанр по ID |
| POST | `/api/genres/` | Создать жанр |
| PUT | `/api/genres/{id}/` | Полное обновление |
| PATCH | `/api/genres/{id}/` | Частичное обновление |
| DELETE | `/api/genres/{id}/` | Soft delete |

### Books

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/books/` | Список книг (пагинация) |
| GET | `/api/books/{id}/` | Книга по ID |
| POST | `/api/books/` | Создать книгу |
| PUT | `/api/books/{id}/` | Полное обновление |
| PATCH | `/api/books/{id}/` | Частичное обновление |
| DELETE | `/api/books/{id}/` | Soft delete |

### Формат ответа книги

```json
{
    "id": 13,
    "uuid": "31df2342-f333-4907-abc6-781fa43665c5",
    "title": "Демон",
    "author": 4,
    "author_name": "Михаил Лермонтов",
    "genre": 3,
    "genre_name": "Классика",
    "year": 1842,
    "status": "issued",
    "description": "Поэма о падшем ангеле, влюбившемся в смертную.",
    "created_at": "2026-10-07T15:41:57.750984Z",
    "updated_at": "2026-10-07T15:41:57.750997Z",
    "deleted_at": null
}
```

---

## Тестирование

### Через cURL

**Список книг:**

```bash
curl.exe "http://127.0.0.1:8000/api/books/?page=1&limit=5"
```

**Создание автора:**

```bash
curl.exe -X POST http://127.0.0.1:8000/api/authors/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Стивен Кинг\", \"birth_year\": 1947, \"country\": \"США\"}"
```

**Создание жанра:**

```bash
curl.exe -X POST http://127.0.0.1:8000/api/genres/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Ужасы\"}"
```

**Создание книги:**

```bash
curl.exe -X POST http://127.0.0.1:8000/api/books/ ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Оно\", \"author\": 1, \"genre\": 1, \"year\": 1986, \"status\": \"available\"}"
```

**Мягкое удаление:**

```bash
curl.exe -X DELETE http://127.0.0.1:8000/api/books/1/
```

**Проверка, что книга скрыта:**

```bash
curl.exe "http://127.0.0.1:8000/api/books/?page=1"
```

### Через Browsable API

Открой в браузере `http://127.0.0.1:8000/api/` — DRF предоставляет интерактивный интерфейс для тестирования всех эндпоинтов.

---

## Контрольные вопросы

### Лаба №1

1. **Клиент-серверная архитектура** — модель взаимодействия, где клиент инициирует запросы, сервер обрабатывает и возвращает ответ. Компоненты: клиент, сервер, сеть, протокол.

2. **HTTP-методы:** GET (получение), POST (создание), PUT (полное обновление), PATCH (частичное обновление), DELETE (удаление), HEAD, OPTIONS.

3. **Статус-коды:** 1xx (информационные), 2xx (успех), 3xx (перенаправления), 4xx (ошибки клиента), 5xx (ошибки сервера). Примеры: 200, 201, 204, 400, 404, 500.

4. **HTTP vs HTTPS:** HTTPS = HTTP + TLS/SSL. Обеспечивает шифрование, аутентификацию сервера, целостность данных.

5. **HTTP-заголовки** — метаданные запроса/ответа: `Content-Type`, `Content-Length`, `Authorization`, `Cache-Control`, `Cookie`.

6. **Контейнеризация** — упаковка приложения с зависимостями в изолированный контейнер. Преимущества: переносимость, изоляция, воспроизводимость.

7. **Образ vs контейнер:** образ — неизменяемый шаблон, контейнер — запущенный экземпляр образа.

8. **Типы данных в теле:** JSON, XML, HTML, Plain Text, Binary, Form Data, Multipart.

9. **Маршрутизация** — сопоставление URL с обработчиками. В Django — через `urls.py`, `path()`, `include()`.

### Лаба №2

1. **REST** — архитектурный стиль. Ресурсы идентифицируются через URI, действия — через HTTP-методы, состояние не хранится на сервере (stateless).

2. **Идемпотентные методы:** GET, PUT, DELETE, HEAD, OPTIONS. Повторный запрос даёт тот же результат, что и однократный.

3. **PUT vs PATCH:** PUT требует полного представления ресурса, PATCH — только изменяемые поля.

4. **Коды состояний:** создание — 201, удаление — 204, ошибка валидации — 400, ресурс не найден — 404, конфликт — 409, внутренняя ошибка — 500.

5. **Soft Delete** — вместо физического удаления ставится метка `deleted_at`. Плюсы: восстановление, аудит, сохранение ссылочной целостности. Минусы: рост БД, обязательная фильтрация в запросах.

6. **Пагинация** — разбиение списка на страницы. Типы: offset-based (`page`/`limit`), cursor-based (`cursor`). Нужна для производительности и UX.

7. **DTO** — объект передачи данных между слоями. Позволяет валидировать, скрывать внутренние поля, разграничивать контракты API и структуру БД.

8. **ORM** — Object-Relational Mapping. Абстракция над SQL, работа с БД через объекты Python. Плюсы: безопасность (защита от SQL-инъекций), миграции, переносимость между СУБД.

9. **Безопасность секретов:** хранить в `.env`, добавлять в `.gitignore`, использовать `.env.example` как шаблон без реальных данных.

10. **Healthcheck** — периодическая проверка готовности контейнера. В Docker Compose позволяет приложению дождаться готовности БД через `depends_on.condition: service_healthy`.

---

## Автор

GitHub: [@live8without8regrets-tech](https://github.com/live8without8regrets-tech)

Курс: «Веб-программирование и мобильные приложения», 2026