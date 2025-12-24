from celery.schedules import crontab
from app.services.celery.celery_main import celery
from datetime import timedelta

celery.conf.beat_schedule = {
    "upload_streams_json": {
        "task": "testing",
        "schedule": timedelta(minutes=2),
        "args": (
            "https://www.twitch.tv/directory",
            ("div", "Layout-sc-1xcs6mc-0 fNsrnJ"),
            [("img", "tw-image", "src", "zat")],
            "testing",
            "DemoSubs.json",
        ),
    },
}
