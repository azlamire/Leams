# Contributing Guidelines

Спасибо за интерес к проекту Leams! Это руководство поможет вам начать вносить свой вклад.

---

## Кодекс поведения

Мы придерживаемся принципов уважительного и инклюзивного сообщества. Ожидаем от всех участников:

- ✅ Уважительного отношения к другим
- ✅ Конструктивной обратной связи
- ✅ Приветствия разнообразия мнений
- ❌ Оскорбительного или дискриминационного поведения
- ❌ Харассмента в любой форме

---

## Как внести вклад

### 🐛 Сообщить об ошибке

1. Проверьте, нет ли уже подобного issue
2. Используйте шаблон Bug Report
3. Укажите:
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версию системы и браузера
   - Логи/скриншоты

### 💡 Предложить новую функцию

1. Откройте Discussion для обсуждения идеи
2. После одобрения создайте Feature Request issue
3. Опишите:
   - Проблему, которую решает фича
   - Предлагаемое решение
   - Альтернативы
   - Примеры из других платформ

### 📝 Улучшить документацию

- Исправления опечаток и грамматики приветствуются
- Добавление примеров и туториалов
- Перевод на другие языки
- Обновление устаревшей информации

### 💻 Внести код

---

## Процесс разработки

### 1. Fork и клонирование

```bash
# Fork репозитория через GitHub UI

# Клонирование вашего fork
git clone https://github.com/YOUR_USERNAME/Leams.git
cd Leams

# Добавление upstream remote
git remote add upstream https://github.com/azlamire/Leams.git
```

### 2. Создание ветки

```bash
# Обновление main из upstream
git checkout main
git pull upstream main

# Создание feature ветки
git checkout -b feature/your-feature-name

# Примеры названий веток:
# - feature/add-chat-emotes
# - fix/stream-disconnection-bug
# - docs/improve-api-documentation
# - refactor/optimize-database-queries
```

### 3. Настройка окружения

**Backend (Python)**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # dev зависимости
```

**Frontend (TypeScript/React)**:
```bash
cd frontend
bun install  # или npm install
```

### 4. Разработка

#### Запуск dev серверов

**Backend**:
```bash
# В корне проекта
docker-compose up -d postgres redis rabbitmq
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
bun run dev  # или npm run dev
```

#### Код-стайл

**Python** (Black + isort + flake8):
```bash
# Форматирование
black backend/
isort backend/

# Проверка
flake8 backend/
mypy backend/
```

**TypeScript** (Prettier + ESLint):
```bash
# Форматирование
bun run format

# Проверка
bun run lint
```

### 5. Тестирование

**Backend**:
```bash
# Запуск всех тестов
pytest

# С coverage
pytest --cov=backend --cov-report=html

# Конкретный файл
pytest tests/test_streams.py

# С выводом print
pytest -s
```

**Frontend**:
```bash
# Unit тесты
bun test

# E2E тесты
bun run test:e2e

# Coverage
bun run test:coverage
```

### 6. Коммит изменений

Следуйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Примеры хороших коммитов:
git commit -m "feat(chat): add emoji picker component"
git commit -m "fix(stream): resolve RTMP disconnection issue #123"
git commit -m "docs: update API authentication guide"
git commit -m "refactor(database): optimize stream queries"
git commit -m "test: add unit tests for user service"
git commit -m "chore: update dependencies"

# Типы коммитов:
# - feat: новая функция
# - fix: исправление бага
# - docs: изменения в документации
# - style: форматирование кода
# - refactor: рефакторинг
# - test: добавление тестов
# - chore: обновление зависимостей, конфигурации
# - perf: улучшение производительности
```

### 7. Push и Pull Request

```bash
# Push в ваш fork
git push origin feature/your-feature-name

# Создайте Pull Request через GitHub UI
```

#### Чеклист PR

- [ ] Код следует стайл-гайдам проекта
- [ ] Добавлены/обновлены тесты
- [ ] Все тесты проходят локально
- [ ] Обновлена документация (если нужно)
- [ ] Коммиты следуют Conventional Commits
- [ ] PR имеет понятное описание изменений
- [ ] Нет merge conflicts с main

#### Шаблон описания PR

```markdown
## Описание
Краткое описание изменений и мотивации.

## Тип изменений
- [ ] Bug fix (не ломает существующую функциональность)
- [ ] New feature (добавляет функциональность)
- [ ] Breaking change (изменения API или поведения)
- [ ] Documentation update

## Связанные Issues
Fixes #123
Related to #456

## Как протестировано?
Опишите тесты, которые вы запустили.

## Screenshots (если UI изменения)
![Before](url)
![After](url)

## Чеклист
- [x] Код прошёл линтеры
- [x] Добавлены тесты
- [x] Обновлена документация
```

---

## Code Review Process

1. **Automated checks**: CI/CD pipeline должен пройти успешно
2. **Manual review**: Минимум 1 maintainer должен одобрить
3. **Feedback**: Отвечайте на комментарии и вносите правки
4. **Merge**: После одобрения maintainer сделает merge

**Время ответа**:
- Первый ответ: в течение 48 часов
- Review: в течение недели
- Сложные PR могут требовать больше времени

---

## Архитектурные решения

### Backend

**Структура проекта**:
```
backend/
├── api/              # API routes
│   ├── v1/
│   │   ├── auth.py
│   │   ├── streams.py
│   │   └── users.py
├── core/             # Core functionality
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/           # SQLModel models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── tests/            # Tests
└── main.py           # Application entry point
```

**Принципы**:
- **Dependency Injection**: Используйте FastAPI's Depends
- **Separation of Concerns**: API → Service → Repository
- **Type Safety**: Pydantic для validation, SQLModel для DB
- **Async First**: Используйте async/await где возможно

**Пример хорошего кода**:
```python
# api/v1/streams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

router = APIRouter()

@router.get("/streams/{stream_id}", response_model=StreamResponse)
async def get_stream(
    stream_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> StreamResponse:
    """Get stream by ID."""
    stream = await stream_service.get_by_id(session, stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return stream
```

### Frontend

**Структура проекта**:
```
frontend/src/
├── app/              # Next.js pages (App Router)
├── features/         # Feature-based modules
│   ├── auth/
│   ├── streams/
│   └── chat/
├── ui/               # Reusable UI components
├── hooks/            # Custom React hooks
├── lib/              # Utilities and integrations
└── shared/           # Shared types and constants
```

**Принципы**:
- **Component Composition**: Переиспользуемые компоненты
- **Type Safety**: TypeScript строгий режим
- **Performance**: React.memo, useMemo, useCallback
- **Accessibility**: ARIA labels, keyboard navigation

**Пример хорошего кода**:
```typescript
// features/streams/components/StreamCard.tsx
import { memo } from 'react';
import type { Stream } from '@/shared/types';

interface StreamCardProps {
  stream: Stream;
  onFollow?: (streamId: string) => void;
}

export const StreamCard = memo<StreamCardProps>(({ stream, onFollow }) => {
  return (
    <article className="stream-card" aria-label={`${stream.username}'s stream`}>
      <img src={stream.thumbnailUrl} alt={stream.title} loading="lazy" />
      <h3>{stream.title}</h3>
      <button onClick={() => onFollow?.(stream.id)}>Follow</button>
    </article>
  );
});
```

---

## Testing Guidelines

### Backend Tests

```python
# tests/test_streams.py
import pytest
from httpx import AsyncClient
from sqlmodel import Session

@pytest.mark.asyncio
async def test_create_stream(client: AsyncClient, auth_headers: dict):
    """Test creating a new stream."""
    response = await client.post(
        "/api/v1/streams",
        headers=auth_headers,
        json={"title": "Test Stream", "category": "Gaming"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Stream"

@pytest.mark.asyncio
async def test_get_stream_not_found(client: AsyncClient):
    """Test getting non-existent stream returns 404."""
    response = await client.get("/api/v1/streams/nonexistent")
    assert response.status_code == 404
```

### Frontend Tests

```typescript
// features/streams/components/StreamCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { StreamCard } from './StreamCard';

describe('StreamCard', () => {
  const mockStream = {
    id: '123',
    title: 'Test Stream',
    username: 'testuser',
    viewerCount: 100,
  };

  it('renders stream information', () => {
    render(<StreamCard stream={mockStream} />);
    expect(screen.getByText('Test Stream')).toBeInTheDocument();
    expect(screen.getByText('testuser')).toBeInTheDocument();
  });

  it('calls onFollow when follow button clicked', () => {
    const onFollow = jest.fn();
    render(<StreamCard stream={mockStream} onFollow={onFollow} />);
    
    fireEvent.click(screen.getByText('Follow'));
    expect(onFollow).toHaveBeenCalledWith('123');
  });
});
```

---

## Performance Guidelines

### Backend
- Используйте индексы БД для часто запрашиваемых полей
- Кэшируйте дорогие операции в Redis
- Используйте pagination для больших списков
- Оптимизируйте N+1 queries (используйте joins)
- Асинхронные операции где возможно

### Frontend
- Lazy load компонентов (`React.lazy()`)
- Оптимизация изображений (Next.js Image)
- Code splitting
- Мемоизация дорогих вычислений
- Virtual scrolling для длинных списков

---

## Security Guidelines

**Всегда проверяйте**:
- Input validation на всех endpoints
- Authentication/Authorization
- SQL injection prevention (используйте ORM)
- XSS protection (sanitize user input)
- CSRF tokens
- Rate limiting
- Secure password hashing (bcrypt)

**Никогда не коммитьте**:
- API keys, secrets, passwords
- `.env` файлы с реальными данными
- Private keys
- Используйте `.env.example` для шаблонов

---

## Дополнительные ресурсы

- [Project Roadmap](https://github.com/azlamire/Leams/projects)
- [Discord сообщество](https://discord.gg/leams)
- [Встречи contributors](https://calendar.google.com/leams-contrib)
- [Design System](https://design.leams.com)

---

## Вопросы?

- GitHub Discussions: https://github.com/azlamire/Leams/discussions
- Discord: https://discord.gg/leams
- Email: contribute@leams.com

**Спасибо за ваш вклад! 🎉**
