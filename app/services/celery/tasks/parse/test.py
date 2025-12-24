from app.utils.parser import parse
from app.services.celery.celery_main import celery
from app.services.s3 import S3Client
from typing import List, Tuple, Literal
import json
import asyncio


async def get_something(
    url: str,
    main: tuple[str, str],
    elements: List[Tuple[str, str, Literal["text", "src"], str]],
    bucket_name: str,
    name_file: str,
):
    something_dict = await parse(
        url=url,
        main=main,
        elements=elements,
    )
    # NOTE: I know that's not correct but just for viewers and None's theme read about it

    if not isinstance(something_dict, type(None)):
        json_format = json.dumps(something_dict, sort_keys=True, indent=4)
        await S3Client(bucket_name=bucket_name).upload_file(
            file=json_format, name_file=name_file
        )
        print(json_format)


@celery.task(name="testing")
def get_test(
    url: str,
    main: tuple[str, str],
    elements: List[Tuple[str, str, Literal["text", "src"], str]],
    bucket_name: str,
    name_file: str,
):
    asyncio.run(
        get_something(
            url=url,
            main=main,
            elements=elements,
            bucket_name=bucket_name,
            name_file=name_file,
        )
    )
