# Auth API

API для авторизации пользователей с ролями и правами доступа.

## Запуск

```
pip install fastapi uvicorn sqlalchemy asyncpg python-jose bcrypt pydantic[email]
uvicorn main:app --reload
```

Swagger: http://localhost:8000/docs

Перед запуском настрой БД в database.py

## Как работает

Есть роли admin и user. Есть бизнес-элементы (products, orders). Для каждой пары роль+элемент задаются права (чтение, создание и тд).

После регистрации у пользователя нет ролей, надо назначить через /users/assign-role.

## Таблицы

- users
- roles
- user_role
- blacklisted_tokens
- business_elements
- access_rules
