from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from app.core.settings import get_s3_settings

s3_settings = get_s3_settings()


class S3Client:
    def __init__(
        self,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": s3_settings.S3_ACCESS_KEY.get_secret_value(),
            "aws_secret_access_key": s3_settings.S3_SECRET_KEY.get_secret_value(),
            "endpoint_url": s3_settings.S3_ENDPOINT_KEY.get_secret_value(),
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        file: str,
        name_file: str,
    ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=name_file,
                Body=file,
            )  # type: ignore

    async def get_file(self, name_file: str):
        async with self.get_client() as client:
            return await client.get_object(Bucket=self.bucket_name, Key=name_file)  # type: ignore
