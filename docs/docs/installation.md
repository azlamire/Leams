# Установка и настройка

## Требования к системе

### Минимальные требования
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk**: 50 GB SSD
- **OS**: Ubuntu 20.04+ / CentOS 8+ / macOS / Windows 10+

### Рекомендуемые требования (Production)
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Disk**: 200+ GB SSD
- **OS**: Ubuntu 22.04 LTS

## Необходимое ПО

- [Docker](https://docs.docker.com/get-docker/) 24.0+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+
- [Git](https://git-scm.com/downloads)
- [Node.js](https://nodejs.org/) 18+ (для frontend разработки)
- [Python](https://www.python.org/) 3.11+ (для backend разработки)

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/azlamire/Leams.git
cd Leams
```

### 2. Настройка переменных окружения

```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование файла с вашими настройками
nano .env
```

**Основные переменные окружения:**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/leams
POSTGRES_USER=leams_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=leams

# Redis
REDIS_URL=redis://localhost:6379/0

# S3 Storage
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=leams-streams

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
BACKEND_PORT=8000
FRONTEND_PORT=3000
NODE_ENV=development
```

### 3. Запуск с Docker Compose

```bash
# Сборка образов
docker-compose build

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### 4. Инициализация базы данных

```bash
# Применение миграций
docker-compose exec backend alembic upgrade head

# Создание начальных данных (опционально)
docker-compose exec backend python scripts/init_db.py
```

### 5. Проверка работоспособности

После запуска сервисы будут доступны по следующим адресам:

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Проверьте health check:
```bash
# Backend health check
curl http://localhost:8000/health

# Ожидаемый ответ
{"status": "healthy"}
```

---

## Локальная разработка (без Docker)

### Backend Setup

```bash
cd backend

# Создание виртуального окружения
python -m venv venv

# Активация окружения
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Установка зависимостей
bun install
# или
npm install

# Запуск dev сервера
bun run dev
# или
npm run dev
```

---

## Устранение распространенных проблем

### Порты уже заняты

Если порты 3000 или 8000 заняты, измените их в `.env`:
```bash
BACKEND_PORT=8080
FRONTEND_PORT=3001
```

### Проблемы с правами доступа Docker

```bash
# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогиньтесь для применения изменений
```

### Ошибки подключения к базе данных

Убедитесь, что PostgreSQL контейнер запущен:
```bash
docker-compose ps postgres
docker-compose logs postgres
```

### Проблемы с миграциями

```bash
# Откат последней миграции
docker-compose exec backend alembic downgrade -1

# Применение заново
docker-compose exec backend alembic upgrade head
```

---

## Следующие шаги

- Ознакомьтесь с [архитектурой проекта](backend/overview.md)
- Изучите [API документацию](api/overview.md)
- Настройте [streaming сервер](streaming/setup.md)
- Прочитайте [руководство по разработке](development/guidelines.md)
