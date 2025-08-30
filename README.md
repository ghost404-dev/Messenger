# Messenger

# 📌 Реализация чата (Django + DRF + Channels + JWT + WebSocket)

## 🚀 Описание проекта
Это проект **мессенджера**, реализованного на Django.  
В нём есть:
- REST API для регистрации и аутентификации пользователей.
- JWT-токены для авторизации.
- WebSocket для общения в реальном времени (через Django Channels).
- Redis как message-broker для обработки событий.
- Поддержка будущего функционала: уведомления, личные диалоги, чаты по заказам, вложения (файлы/изображения).

---

## ⚙️ Используемый стек
### Бэкенд
- **Python 3.12+**
- **Django 5**
- **Django REST Framework**
- **Django Channels**
- **Redis** (как backend для Channels)
- **PostgreSQL** (БД)
- **SimpleJWT** (JWT-аутентификация)

### Фронтенд (планируется)
- **React (TypeScript)**
- **WebSocket client** (подключение к Channels)

### Инфраструктура
- **Docker** (планируется для Redis + PostgreSQL)
- **NGINX / Daphne** (деплой)

---

## 📂 Структура проекта
```
├── LICENSE
├── project
│   ├── chat
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── __init__.py
│   │   ├── middleware.py
│   │   ├── models.py
│   │   ├── routing.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls_messages.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings
│   │   │   ├── base.py
│   │   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── users
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── pyproject.toml
├── README.md
└── uv.lock
```
---

## 🔑 Реализовано на данный момент
1. **Регистрация пользователя** через DRF:
   - POST `/api/register/`
   - Создаётся новый пользователь.
2. **Аутентификация (JWT)**:
   - POST `/api/token/` → получить `access` и `refresh`.
   - POST `/api/token/refresh/` → обновить `access`.
3. **Подключение к WebSocket**:
   - URL: `ws://localhost:8000/ws/chat/<room_name>/?token=<JWT>`
   - Авторизация через JWT.
   - Поддержка `send/receive` сообщений.
4. **Базовый чат** (отправка сообщений в комнату).

---

## 📡 API эндпоинты
### 🔐 Аутентификация
- `POST /api/register/` — регистрация нового пользователя
- `POST /api/token/` — получение JWT токена
- `POST /api/token/refresh/` — обновление access-токена

### 💬 Чат (WebSocket)
- Подключение:
ws://localhost:8000/ws/chat/<room_name>/?token=<JWT>
- Формат сообщений (JSON):
```
{
  "message": "Привет, мир!"
}
```
Ответ
```
{
  "user": "ghost",
  "message": "Привет, мир!",
  "timestamp": "2025-08-30 12:00:00"
}
```

✅ (сделано) Регистрация, JWT, WS.

🔲 Хранение сообщений в БД (связка с User и ChatRoom).

✅ Личные диалоги (user-to-user).

🔲 Система уведомлений (новое сообщение → пуш/сигнал).

🔲 Поддержка вложений (файлы, картинки).

🔲 Админ-панель для управления чатами.

🔲 Docker + NGINX деплой.
