# Development Guidelines

Руководство по разработке для контрибьюторов проекта Leams.

---

## Настройка окружения

### Требования

- **Docker** 24.0+
- **Docker Compose** 2.0+
- **Git** 2.x
- **Python** 3.11+ (для backend разработки)
- **Node.js** 18+ или **Bun** 1.0+ (для frontend разработки)
- **VS Code** или **PyCharm** (рекомендуется)

### Клонирование и настройка

```bash
# Клонирование репозитория
git clone https://github.com/azlamire/Leams.git
cd Leams

# Создание .env файла
cp .env.example .env

# Запуск инфраструктуры
docker-compose up -d postgres redis rabbitmq elasticsearch minio

# Подождите ~30 секунд пока сервисы запустятся
docker-compose ps
```

---

## Backend разработка

### Установка зависимостей

```bash
cd backend

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Структура проекта

```
backend/
├── alembic/              # Database migrations
├── api/
│   └── v1/               # API version 1
│       ├── auth.py       # Authentication endpoints
│       ├── streams.py    # Stream endpoints
│       ├── users.py      # User endpoints
│       └── chat.py       # Chat endpoints
├── core/
│   ├── config.py         # Configuration
│   ├── security.py       # Security utilities (JWT, hashing)
│   └── database.py       # Database connection
├── models/               # SQLModel database models
│   ├── user.py
│   ├── stream.py
│   └── chat.py
├── schemas/              # Pydantic request/response schemas
│   ├── user.py
│   ├── stream.py
│   └── auth.py
├── services/             # Business logic
│   ├── auth_service.py
│   ├── stream_service.py
│   └── user_service.py
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   ├── test_auth.py
│   ├── test_streams.py
│   └── test_users.py
└── main.py               # Application entry point
```

### Запуск dev сервера

```bash
# Применение миграций
alembic upgrade head

# Запуск сервера с hot-reload
uvicorn main:app --reload --port 8000

# Доступ к API:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - OpenAPI schema: http://localhost:8000/openapi.json
```

### Создание нового endpoint

```python
# api/v1/example.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from core.database import get_session
from core.security import get_current_user
from models.user import User
from schemas.example import ExampleCreate, ExampleResponse
from services.example_service import ExampleService

router = APIRouter()

@router.post("/examples", response_model=ExampleResponse, status_code=201)
async def create_example(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    example_in: ExampleCreate
) -> ExampleResponse:
    """Create a new example."""
    example = await ExampleService.create(
        session=session,
        user_id=current_user.id,
        data=example_in
    )
    return example

@router.get("/examples", response_model=List[ExampleResponse])
async def list_examples(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 20
) -> List[ExampleResponse]:
    """List examples with pagination."""
    examples = await ExampleService.get_multi(
        session=session,
        skip=skip,
        limit=limit
    )
    return examples
```

### Database миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Add new table"

# Применение миграций
alembic upgrade head

# Откат последней миграции
alembic downgrade -1

# История миграций
alembic history

# Текущая версия
alembic current
```

### Тестирование

```bash
# Запуск всех тестов
pytest

# С coverage отчетом
pytest --cov=backend --cov-report=html
open htmlcov/index.html

# Конкретный файл
pytest tests/test_streams.py

# Конкретный тест
pytest tests/test_streams.py::test_create_stream

# С выводом print statements
pytest -s

# Параллельное выполнение
pytest -n auto
```

### Линтинг и форматирование

```bash
# Black - форматирование кода
black backend/

# isort - сортировка импортов
isort backend/

# flake8 - проверка стиля
flake8 backend/

# mypy - type checking
mypy backend/

# Все проверки разом
black backend/ && isort backend/ && flake8 backend/ && mypy backend/
```

### Pre-commit hooks

```bash
# Установка
pip install pre-commit
pre-commit install

# Теперь при каждом коммите автоматически:
# - Black форматирование
# - isort сортировка импортов
# - flake8 проверки
# - mypy type checks
```

---

## Frontend разработка

### Установка зависимостей

```bash
cd frontend

# Используйте Bun (рекомендуется)
bun install

# Или npm
npm install
```

### Структура проекта

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── streams/            # Streams pages
│   │   │   ├── page.tsx        # /streams
│   │   │   └── [id]/           # /streams/:id
│   │   │       └── page.tsx
│   │   └── profile/
│   │       └── page.tsx
│   │
│   ├── features/               # Feature modules
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── api/
│   │   │   └── types.ts
│   │   ├── streams/
│   │   └── chat/
│   │
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── Card.tsx
│   │
│   ├── hooks/                  # Shared hooks
│   │   ├── useAuth.ts
│   │   ├── useWebSocket.ts
│   │   └── useMediaQuery.ts
│   │
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client
│   │   ├── utils.ts            # Helper functions
│   │   └── constants.ts
│   │
│   └── shared/                 # Shared types
│       └── types.ts
│
├── public/                     # Static files
├── tests/                      # Tests
└── playwright.config.ts        # E2E config
```

### Запуск dev сервера

```bash
# Development server
bun run dev
# или
npm run dev

# Доступ: http://localhost:3000
```

### Создание нового компонента

```typescript
// src/ui/Button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'rounded-lg font-medium transition-colors',
          {
            'bg-purple-600 hover:bg-purple-700 text-white': variant === 'primary',
            'bg-gray-200 hover:bg-gray-300 text-gray-900': variant === 'secondary',
            'hover:bg-gray-100': variant === 'ghost',
          },
          {
            'px-3 py-1.5 text-sm': size === 'sm',
            'px-4 py-2 text-base': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';
```

### API интеграция

```typescript
// src/features/streams/api/getStreams.ts
import { apiClient } from '@/lib/api';
import type { Stream } from '@/shared/types';

interface GetStreamsParams {
  limit?: number;
  offset?: number;
  category?: string;
}

export async function getStreams(params?: GetStreamsParams): Promise<Stream[]> {
  const response = await apiClient.get<{ streams: Stream[] }>('/streams/live', {
    params,
  });
  return response.data.streams;
}

// Использование с TanStack Query
import { useQuery } from '@tanstack/react-query';

export function useStreams(params?: GetStreamsParams) {
  return useQuery({
    queryKey: ['streams', params],
    queryFn: () => getStreams(params),
    staleTime: 30000, // 30 seconds
  });
}
```

### Тестирование

```bash
# Unit tests (Jest + React Testing Library)
bun test
# или
npm test

# E2E tests (Playwright)
bun run test:e2e
# или
npm run test:e2e

# Coverage
bun run test:coverage
```

**Пример unit теста:**

```typescript
// src/ui/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick handler', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    
    fireEvent.click(screen.getByText('Click'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant styles', () => {
    render(<Button variant="primary">Primary</Button>);
    const button = screen.getByText('Primary');
    expect(button).toHaveClass('bg-purple-600');
  });
});
```

### Линтинг и форматирование

```bash
# ESLint
bun run lint
# или
npm run lint

# Prettier
bun run format
# или
npm run format

# Type check
bun run type-check
# или
npm run type-check
```

---

## Git Workflow

### Branch naming

```
feature/add-stream-chat
fix/resolve-disconnection-bug
docs/update-api-guide
refactor/optimize-queries
test/add-auth-tests
chore/update-dependencies
```

### Commit messages

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat(chat): add emoji picker component
fix(stream): resolve RTMP disconnection issue
docs: update installation guide
refactor(api): optimize database queries
test(auth): add JWT validation tests
chore: update dependencies to latest versions
```

**Типы коммитов:**
- `feat`: новая функциональность
- `fix`: исправление бага
- `docs`: изменения в документации
- `style`: форматирование кода (не влияет на логику)
- `refactor`: рефакторинг кода
- `test`: добавление или изменение тестов
- `chore`: обновление зависимостей, конфигурации
- `perf`: улучшение производительности

### Pull Request процесс

1. Создайте feature branch из `main`
2. Внесите изменения с понятными коммитами
3. Добавьте тесты для новой функциональности
4. Убедитесь что все тесты проходят
5. Запустите линтеры и форматтеры
6. Push в ваш fork
7. Создайте Pull Request с описанием изменений

---

## Debugging

### Backend debugging (VS Code)

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

### Frontend debugging (Browser DevTools)

```typescript
// Включите Source Maps в next.config.js
const nextConfig = {
  productionBrowserSourceMaps: true,
};
```

### Database debugging

```bash
# Подключение к PostgreSQL
docker-compose exec postgres psql -U leams_user -d leams

# Проверка данных
SELECT * FROM users LIMIT 5;
SELECT * FROM streams WHERE is_live = true;

# Проверка индексов
\di

# Анализ запроса
EXPLAIN ANALYZE SELECT * FROM streams WHERE user_id = 'xxx';
```

### Redis debugging

```bash
# Подключение к Redis
docker-compose exec redis redis-cli

# Просмотр ключей
KEYS *

# Получение значения
GET user:session:abc123

# Мониторинг команд
MONITOR
```

---

## Performance Optimization

### Backend

- Используйте async/await для I/O операций
- Добавьте индексы для часто запрашиваемых полей
- Кэшируйте дорогие запросы в Redis
- Используйте connection pooling для БД
- Оптимизируйте N+1 queries

**Пример оптимизации:**

```python
# ❌ Плохо - N+1 query
streams = session.exec(select(Stream)).all()
for stream in streams:
    user = session.get(User, stream.user_id)  # N запросов

# ✅ Хорошо - JOIN
statement = (
    select(Stream, User)
    .join(User, Stream.user_id == User.id)
)
results = session.exec(statement).all()
```

### Frontend

- Lazy load компонентов
- Используйте React.memo для дорогих компонентов
- Мемоизация с useMemo/useCallback
- Оптимизация изображений (Next.js Image)
- Code splitting
- Virtual scrolling для длинных списков

**Пример оптимизации:**

```typescript
// ❌ Плохо - re-renders on every parent render
function StreamList({ streams }) {
  return streams.map(stream => (
    <StreamCard key={stream.id} stream={stream} />
  ));
}

// ✅ Хорошо - memoized component
const StreamCard = memo(({ stream }) => {
  // ...
});

function StreamList({ streams }) {
  return streams.map(stream => (
    <StreamCard key={stream.id} stream={stream} />
  ));
}
```

---

## Полезные команды

### Docker

```bash
# Перезапуск всех сервисов
docker-compose restart

# Просмотр логов
docker-compose logs -f [service_name]

# Очистка volumes
docker-compose down -v

# Rebuild конкретного сервиса
docker-compose up -d --build backend
```

### Database

```bash
# Создание backup
docker-compose exec postgres pg_dump -U leams_user leams > backup.sql

# Восстановление из backup
docker-compose exec -T postgres psql -U leams_user leams < backup.sql
```

---

## Дополнительные ресурсы

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
