from app.utils.parser import parse
from app.core.celery_main import celery
from app.services.s3 import S3Client
import json


async def get_category():
    category_dict = await parse(
        url="https://www.twitch.tv/directory",
        main=("div", "Layout-sc-1xcs6mc-0 fNsrnJ"),
        elements=[("img", "tw-image", "src")],
    )
    # NOTE: I know that's not correct but just for viewers and None's theme read about it

    if not isinstance(category_dict, type(None)):
        json_format = json.dumps(category_dict)
        await S3Client(bucket_name="testing").upload_file(
            file=json_format, name_file="category"
        )
