from celery import Celery
from celery.schedules import crontab

# IDK: Why but when celery -A ... usage it's not correct and need
# to use like app.core.settings like it returns back in path nub
# When python used just from settings is correct
from app.core.settings import get_redis_settings

redis_settings = get_redis_settings()
# IDK: In services.auth.oauth github doesn't requrie get_secret_value but here..
celery = Celery(
    __name__,
    broker=redis_settings.BROKER.get_secret_value(),
    backend=redis_settings.BACKEND_REDIS.get_secret_value(),
)

import app.services.celery.beat_config
import app.services.celery.tasks.sample_parse
