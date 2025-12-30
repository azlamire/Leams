from app.services.celery.celery_main import celery
from datetime import timedelta

celery.conf.beat_schedule = {
    "upload_categories": {
        "task": "download_categories",
        "schedule": timedelta(minutes=1),
        "args": (
            "https://www.twitch.tv/directory",
            ("div", "Layout-sc-1xcs6mc-0 fNsrnJ"),
            [
                ("img", "tw-image", "src", "image"),
                ("h2", "CoreText-sc-1txzju1-0 erESIP", "text", "name"),
            ],
            "testing",
        ),
    }
}
