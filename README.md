# Auth API

REST API для аутентификации и авторизации пользователей с системой ролей и прав доступа.

## Технологии

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** (async) — ORM
- **JWT** — аутентификация
- **Docker / Docker Compose** — контейнеризация
- **Bcrypt** — хеширование паролей

## Возможности

- Регистрация и вход пользователей
- JWT-токены + блэклист (logout)
- Система ролей: `admin` и `user`
- Права доступа к бизнес-элементам (products, orders)
- Назначение ролей администратором

## Запуск через Docker

1. Клонировать репозиторий:
```bash
git clone https://github.com/illluminatik/Auth_API.git
cd Auth_API
```

2. Создать `.env` файл (пример в `.env.example`):
```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+asyncpg://postgres:1234@db:5432/auth_db
```

3. Запустить:
```bash
docker-compose up --build
```

4. Открыть Swagger документацию: [http://localhost:8000/docs](http://localhost:8000/docs)

## Эндпоинты

### Пользователи
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/users/register` | Регистрация |
| POST | `/users/login` | Вход, получение токена |
| POST | `/users/logout` | Выход, токен в блэклист |
| GET | `/users/me` | Текущий пользователь |

### Бизнес-элементы
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/products` | Список товаров |
| GET | `/orders` | Список заказов |

### Админ
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/users/assign-role` | Назначить роль пользователю |

## Структура проекта
```
├── main.py           # Точка входа
├── auth.py           # JWT логика
├── database.py       # Подключение к БД
├── models/           # Модели SQLAlchemy
├── routers/          # Роуты (users, business, admin)
├── schemas/          # Pydantic схемы
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```