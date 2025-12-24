from app.utils.parser import parse
from app.core.celery_main import celery
from app.services.s3 import S3Client
import json


async def get_streams():
    streams_dict = await parse(
        url="https://www.twitch.tv/",
        main=(
            "a",
            "ScCoreLink-sc-16kq0mq-0 fytYW InjectLayout-sc-1i43xsx-0 cnzybN side-nav-card__link tw-link",
        ),
        elements=[
            (
                "p",
                "CoreText-sc-1txzju1-0 dTdgXA InjectLayout-sc-1i43xsx-0 hnBAak",
                "text",
            ),
            ("p", "CoreText-sc-1txzju1-0 iMyVXK", "text"),
            (
                "img",
                "InjectLayout-sc-1i43xsx-0 fAYJcN tw-image tw-image-avatar",
                "src",
            ),
        ],
    )

    if not isinstance(streams_dict, type(None)):
        json_format = json.dumps(streams_dict)
        await S3Client(bucket_name="testing").upload_file(
            file=json_format, name_file="category"
        )
