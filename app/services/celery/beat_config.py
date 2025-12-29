from celery.schedules import crontab
from app.services.celery.celery_main import celery
from datetime import timedelta

celery.conf.beat_schedule = {
    "upload_categories": {
        "task": "parse_category",
        "schedule": timedelta(minutes=2),
        "args": (
            "https://www.twitch.tv/directory",
            ("div", "Layout-sc-1xcs6mc-0 fNsrnJ"),
            [("img", "tw-image", "src", "zat")],
            "testing",
            "Category.json",
        ),
    },
    "upload_streams_json": {
        "task": "parse_json_streams",
        "schedule": timedelta(minutes=2),
        "args": (
            "https://www.twitch.tv",
            ("article", "Layout-sc-1xcs6mc-0 ghbJdj"),
            [
                ("img", "tw-image", "src", "img"),
                ("h4", "CoreText-sc-1txzju1-0 kVxrzL", "text", "title"),
                (
                    "img",
                    "InjectLayout-sc-1i43xsx-0 fAYJcN tw-image tw-image-avatar",
                    "src",
                    "avatar",
                ),
                ("p", "CoreText-sc-1txzju1-0 kdDAY", "text", "name"),
            ],
            "testing",
            "DemoStreams.json",
        ),
    },
}
