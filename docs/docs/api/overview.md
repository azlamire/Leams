# API Documentation

## Обзор API

Leams предоставляет RESTful API построенный на FastAPI, с автоматической генерацией документации OpenAPI/Swagger.

**Base URL**: `https://api.leams.com/v1` (production) или `http://localhost:8000` (development)

**API Documentation**:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI Schema: `/openapi.json`

---

## Аутентификация

API использует JWT (JSON Web Tokens) для аутентификации.

### Получение токенов

**Endpoint**: `POST /auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Использование токенов

Добавьте токен в заголовок Authorization для защищенных эндпоинтов:

```http
Authorization: Bearer <access_token>
```

**Пример с curl**:
```bash
curl -H "Authorization: Bearer eyJhbGci..." \
     https://api.leams.com/v1/user/profile
```

### Обновление токена

**Endpoint**: `POST /auth/refresh`

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Основные эндпоинты

### Authentication & Users

#### Регистрация
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newstreamer",
  "email": "streamer@example.com",
  "password": "securepass123"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "newstreamer",
  "email": "streamer@example.com",
  "created_at": "2025-12-08T10:30:00Z",
  "is_verified": false
}
```

#### Получение профиля
```http
GET /user/profile
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "coolstreamer",
  "display_name": "Cool Streamer",
  "avatar_url": "https://cdn.leams.com/avatars/abc123.jpg",
  "bio": "Gaming streamer focused on FPS games",
  "follower_count": 1250,
  "following_count": 89,
  "stream_key": "live_sk_abc123xyz",
  "is_partner": false,
  "created_at": "2024-01-15T08:00:00Z"
}
```

#### Обновление профиля
```http
PATCH /user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "display_name": "New Display Name",
  "bio": "Updated bio",
  "avatar_url": "https://cdn.leams.com/avatars/new.jpg"
}
```

---

### Streams

#### Список live стримов
```http
GET /streams/live?limit=20&offset=0&category=gaming
```

**Query Parameters**:
- `limit` (int, default: 20): Количество результатов
- `offset` (int, default: 0): Смещение для пагинации
- `category` (string, optional): Фильтр по категории
- `language` (string, optional): Фильтр по языку

**Response** (200 OK):
```json
{
  "total": 156,
  "limit": 20,
  "offset": 0,
  "streams": [
    {
      "id": "stream_123",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "coolstreamer",
      "title": "Playing CS2 Ranked",
      "category": "Counter-Strike 2",
      "viewer_count": 1234,
      "thumbnail_url": "https://cdn.leams.com/thumbnails/stream_123.jpg",
      "started_at": "2025-12-08T14:30:00Z",
      "language": "en",
      "is_mature": false,
      "tags": ["fps", "competitive", "english"]
    }
  ]
}
```

#### Информация о стриме
```http
GET /streams/{stream_id}
```

**Response** (200 OK):
```json
{
  "id": "stream_123",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "coolstreamer",
    "display_name": "Cool Streamer",
    "avatar_url": "https://cdn.leams.com/avatars/abc.jpg"
  },
  "title": "Playing CS2 Ranked - Road to Global Elite",
  "description": "Grinding to Global Elite rank!",
  "category": "Counter-Strike 2",
  "viewer_count": 1234,
  "is_live": true,
  "started_at": "2025-12-08T14:30:00Z",
  "thumbnail_url": "https://cdn.leams.com/thumbnails/stream_123.jpg",
  "stream_url": "https://cdn.leams.com/live/stream_123/index.m3u8",
  "chat_url": "wss://chat.leams.com/stream_123",
  "language": "en",
  "is_mature": false,
  "tags": ["fps", "competitive", "english"]
}
```

#### Создание/обновление стрима
```http
PUT /streams
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Morning stream - Chill gameplay",
  "category": "Just Chatting",
  "description": "Relaxing morning stream",
  "tags": ["english", "chill", "morning"],
  "is_mature": false
}
```

**Response** (200 OK):
```json
{
  "id": "stream_456",
  "title": "Morning stream - Chill gameplay",
  "rtmp_url": "rtmp://ingest.leams.com/live",
  "stream_key": "live_sk_abc123xyz",
  "updated_at": "2025-12-08T15:00:00Z"
}
```

#### Завершение стрима
```http
DELETE /streams/current
Authorization: Bearer <token>
```

**Response** (204 No Content)

---

### VODs (Video on Demand)

#### Список VODs пользователя
```http
GET /users/{username}/vods?limit=10&offset=0
```

**Response** (200 OK):
```json
{
  "total": 45,
  "vods": [
    {
      "id": "vod_789",
      "title": "Epic CS2 Comeback - Full Match",
      "thumbnail_url": "https://cdn.leams.com/vods/vod_789_thumb.jpg",
      "duration": 7234,
      "view_count": 5678,
      "created_at": "2025-12-07T20:00:00Z",
      "video_url": "https://cdn.leams.com/vods/vod_789/index.m3u8"
    }
  ]
}
```

#### Получение VOD
```http
GET /vods/{vod_id}
```

**Response** (200 OK):
```json
{
  "id": "vod_789",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "coolstreamer"
  },
  "title": "Epic CS2 Comeback - Full Match",
  "description": "Watch how we came back from 3-12!",
  "duration": 7234,
  "view_count": 5678,
  "thumbnail_url": "https://cdn.leams.com/vods/vod_789_thumb.jpg",
  "video_url": "https://cdn.leams.com/vods/vod_789/index.m3u8",
  "created_at": "2025-12-07T20:00:00Z",
  "categories": ["Counter-Strike 2"],
  "tags": ["fps", "comeback", "clutch"]
}
```

---

### Following & Subscriptions

#### Follow пользователя
```http
POST /users/{username}/follow
Authorization: Bearer <token>
```

**Response** (201 Created):
```json
{
  "following": true,
  "followed_at": "2025-12-08T15:30:00Z"
}
```

#### Unfollow пользователя
```http
DELETE /users/{username}/follow
Authorization: Bearer <token>
```

**Response** (204 No Content)

#### Список подписок
```http
GET /user/following?limit=50&offset=0
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "total": 23,
  "following": [
    {
      "user_id": "abc-123",
      "username": "streamer1",
      "display_name": "Streamer One",
      "avatar_url": "https://cdn.leams.com/avatars/streamer1.jpg",
      "is_live": true,
      "followed_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

### Chat

#### Получение истории чата
```http
GET /chat/{stream_id}/messages?limit=100&before={message_id}
```

**Response** (200 OK):
```json
{
  "messages": [
    {
      "id": "msg_001",
      "user": {
        "id": "user_123",
        "username": "viewer123",
        "display_name": "Viewer 123",
        "badges": ["subscriber", "moderator"]
      },
      "message": "Great stream! PogChamp",
      "emotes": [
        {
          "name": "PogChamp",
          "url": "https://cdn.leams.com/emotes/pogchamp.png",
          "positions": [[14, 22]]
        }
      ],
      "timestamp": "2025-12-08T15:45:32Z"
    }
  ]
}
```

#### WebSocket подключение к чату
```
wss://chat.leams.com/stream/{stream_id}?token={jwt_token}
```

**Отправка сообщения**:
```json
{
  "type": "message",
  "data": {
    "message": "Hello chat!"
  }
}
```

**Получение сообщения**:
```json
{
  "type": "message",
  "data": {
    "id": "msg_002",
    "user": {
      "username": "viewer456",
      "display_name": "Viewer 456"
    },
    "message": "Hello!",
    "timestamp": "2025-12-08T15:46:00Z"
  }
}
```

---

### Search

#### Поиск стримов и пользователей
```http
GET /search?q=counter+strike&type=streams,users&limit=20
```

**Query Parameters**:
- `q` (string, required): Поисковый запрос
- `type` (string, default: "streams,users"): Типы результатов
- `limit` (int, default: 20): Количество результатов

**Response** (200 OK):
```json
{
  "streams": [
    {
      "id": "stream_999",
      "username": "csplayer",
      "title": "Counter-Strike 2 Pro Gameplay",
      "viewer_count": 890,
      "thumbnail_url": "..."
    }
  ],
  "users": [
    {
      "id": "user_888",
      "username": "counterstrike_fan",
      "display_name": "CS Fan",
      "follower_count": 450
    }
  ]
}
```

---

## Rate Limits

| Endpoint Type | Limit |
|--------------|-------|
| Authenticated | 1000 requests / hour |
| Unauthenticated | 100 requests / hour |
| Search | 30 requests / minute |
| Chat messages | 20 messages / 30 seconds |

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1701180000
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Успешный запрос |
| 201 | Created - Ресурс создан |
| 204 | No Content - Успех без тела ответа |
| 400 | Bad Request - Неверные параметры |
| 401 | Unauthorized - Требуется аутентификация |
| 403 | Forbidden - Доступ запрещен |
| 404 | Not Found - Ресурс не найден |
| 429 | Too Many Requests - Rate limit превышен |
| 500 | Internal Server Error - Ошибка сервера |

---

## Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request parameters are invalid",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

---

## Webhooks

Для получения событий в реальном времени, настройте webhooks в настройках разработчика.

### События

- `stream.online` - Стрим начался
- `stream.offline` - Стрим завершился
- `user.follow` - Новый подписчик
- `user.subscribe` - Новая подписка

**Пример payload**:
```json
{
  "event": "stream.online",
  "timestamp": "2025-12-08T16:00:00Z",
  "data": {
    "user_id": "user_123",
    "username": "coolstreamer",
    "stream_id": "stream_999",
    "title": "Back online!"
  }
}
```

---

## SDK и Libraries

- **Python**: `pip install leams-sdk`
- **JavaScript/TypeScript**: `npm install @leams/sdk`
- **Go**: `go get github.com/leams/leams-go`

**Пример использования (Python)**:
```python
from leams import LeamsClient

client = LeamsClient(access_token="your_token")

# Получить live стримы
streams = client.streams.get_live(limit=10)

# Обновить информацию о стриме
client.streams.update(
    title="New Stream Title",
    category="Gaming"
)
```

---

## Дополнительные ресурсы

- [Примеры кода](https://github.com/azlamire/leams-examples)
- [Postman Collection](https://postman.leams.com)
- [GraphQL API](graphql.md) (экспериментально)
- [API Changelog](changelog.md)
