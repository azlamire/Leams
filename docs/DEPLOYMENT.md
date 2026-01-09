# Руководство по развертыванию Leams

## Требования к системе

### Минимальные требования
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB SSD
- OS: Ubuntu 20.04+ / CentOS 8+ / macOS

### Рекомендуемые требования (Production)
- CPU: 8+ cores
- RAM: 16+ GB
- Disk: 200+ GB SSD
- OS: Ubuntu 22.04 LTS

## Необходимое ПО

- Docker 24.0+
- Docker Compose 2.0+
- kubectl 1.28+ (для Kubernetes)
- Git

## Локальная разработка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd Leams
```

### 2. Настройка окружения
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование переменных окружения
nano .env
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
# Запуск миграций
docker-compose exec user-service ./migrate up
docker-compose exec course-service ./migrate up
docker-compose exec assignment-service ./migrate up
```

### 5. Проверка работоспособности
```bash
# Health check API Gateway
curl http://localhost:8080/health

# Health check User Service
curl http://localhost:8081/health
```

## Production развертывание

### Вариант 1: Docker Compose (для малых и средних проектов)

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установка Docker Compose
sudo apt install docker-compose-plugin
```

#### 2. Настройка SSL/TLS
```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d leams.com -d api.leams.com
```

#### 3. Настройка production конфигурации
```bash
# Создание production .env
cp .env.production.example .env.production

# Редактирование конфигурации
nano .env.production
```

#### 4. Запуск в production
```bash
# Использование production конфигурации
docker-compose -f docker-compose.prod.yml up -d

# Настройка автозапуска
sudo systemctl enable docker
```

### Вариант 2: Kubernetes (для высоконагруженных систем)

#### 1. Подготовка Kubernetes кластера
```bash
# Пример для AWS EKS
eksctl create cluster \
  --name leams-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5
```

#### 2. Установка необходимых компонентов
```bash
# Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Cert Manager для SSL
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

#### 3. Создание namespace
```bash
kubectl create namespace leams
kubectl config set-context --current --namespace=leams
```

#### 4. Настройка secrets
```bash
# Создание secrets для БД
kubectl create secret generic db-credentials \
  --from-literal=postgres-password=<password> \
  --from-literal=mongo-password=<password>

# Создание secrets для JWT
kubectl create secret generic jwt-secret \
  --from-literal=jwt-key=<secret-key>
```

#### 5. Развертывание сервисов
```bash
# Применение конфигураций
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/mongodb/
kubectl apply -f k8s/redis/
kubectl apply -f k8s/rabbitmq/

# Развертывание микросервисов
kubectl apply -f k8s/services/
```

#### 6. Настройка Ingress
```bash
kubectl apply -f k8s/ingress.yaml
```

## База данных

### Миграции

#### Создание новой миграции
```bash
# User Service
migrate create -ext sql -dir services/user-service/migrations -seq create_users_table

# Course Service
migrate create -ext sql -dir services/course-service/migrations -seq create_courses_table
```

#### Применение миграций
```bash
# В Docker
docker-compose exec user-service ./migrate up

# Напрямую
migrate -path services/user-service/migrations \
  -database "postgres://user:pass@localhost:5432/leams_users?sslmode=disable" \
  up
```

### Бэкапы

#### PostgreSQL
```bash
# Создание бэкапа
docker-compose exec postgres pg_dump -U postgres leams_users > backup.sql

# Восстановление
docker-compose exec -T postgres psql -U postgres leams_users < backup.sql
```

#### MongoDB
```bash
# Создание бэкапа
docker-compose exec mongodb mongodump --out /backup

# Восстановление
docker-compose exec mongodb mongorestore /backup
```

## Мониторинг

### Prometheus + Grafana

```bash
# Запуск стека мониторинга
docker-compose -f docker-compose.monitoring.yml up -d

# Доступ к Grafana
# URL: http://localhost:3000
# Login: admin
# Password: admin
```

### Метрики приложения

Каждый сервис экспортирует метрики на endpoint `/metrics`:
- User Service: http://localhost:8081/metrics
- Course Service: http://localhost:8082/metrics
- etc.

## Логирование

### ELK Stack

```bash
# Запуск ELK
docker-compose -f docker-compose.logging.yml up -d

# Kibana доступен на
# http://localhost:5601
```

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f user-service

# Последние N строк
docker-compose logs --tail=100 user-service
```

## Масштабирование

### Docker Compose
```bash
# Масштабирование конкретного сервиса
docker-compose up -d --scale user-service=3
```

### Kubernetes
```bash
# Horizontal Pod Autoscaler
kubectl autoscale deployment user-service \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Ручное масштабирование
kubectl scale deployment user-service --replicas=5
```

## Обновление

### Zero-downtime deployment

```bash
# Docker Compose
docker-compose pull
docker-compose up -d --no-deps --build <service-name>

# Kubernetes rolling update
kubectl set image deployment/user-service \
  user-service=leams/user-service:v2.0.0

# Откат при необходимости
kubectl rollout undo deployment/user-service
```

## Безопасность

### Checklist для production

- [ ] Все пароли сгенерированы и безопасно хранятся
- [ ] SSL/TLS настроен для всех публичных endpoints
- [ ] Firewall настроен (только необходимые порты открыты)
- [ ] Rate limiting настроен
- [ ] Регулярные бэкапы настроены
- [ ] Мониторинг и алерты настроены
- [ ] Логирование настроено
- [ ] CORS правильно настроен
- [ ] Secrets не закоммичены в Git

## Устранение неполадок

### Сервис не запускается
```bash
# Проверка логов
docker-compose logs <service-name>

# Проверка сети
docker network ls
docker network inspect leams_default

# Проверка volumes
docker volume ls
```

### Проблемы с БД
```bash
# Проверка подключения к PostgreSQL
docker-compose exec postgres psql -U postgres -c "SELECT 1"

# Проверка MongoDB
docker-compose exec mongodb mongosh --eval "db.runCommand({ ping: 1 })"
```

### Проблемы с производительностью
```bash
# Мониторинг ресурсов
docker stats

# Kubernetes
kubectl top nodes
kubectl top pods
```

## Контакты поддержки

Для получения помощи:
- GitHub Issues: <repository-url>/issues
- Email: support@leams.com
- Slack: leams-dev.slack.com
