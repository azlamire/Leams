import pytest
from app.models.auth import StreamList
from sqlalchemy import select

pytestmark = pytest.mark.anyio


class TestStreamCreation:
    """Тесты для POST /stream_creation"""

    async def test_on_publish_success(self, client):
        """Успешный webhook от nginx-rtmp"""
        response = await client.post(
            "/stream_creation",
            data={
                "app": "live",
                "name": "test_stream",
                "tcurl": "rtmp://localhost/live",
                "addr": "127.0.0.1",
            },
        )
        assert response.status_code == 200
        assert response.json() == "OK"

    async def test_on_publish_missing_fields(self, client):
        """Отсутствуют необязательные поля"""
        response = await client.post(
            "/stream_creation", data={"app": "live", "name": "test_stream"}
        )
        assert response.status_code == 200


class TestStreamEnding:
    async def test_on_publish_done_deletes(self, client, db_session):
        stream = StreamList(stream="to_delete_stream")
        db_session.add(stream)
        await db_session.commit()
        response = await client.post(
            "/stream_ending", data={"app": "live", "name": "to_delete_stream"}
        )
        await db_session.commit()
        result = await db_session.execute(
            select(StreamList).where(StreamList.stream == "to_delete_stream")
        )
        assert result.scalars().first() is None
        assert response.status_code == 200

    async def test_on_publish_done_not_found(self, client):
        response = await client.post(
            "/stream_ending", data={"app": "live", "name": "nonexistent_stream"}
        )
        assert response.status_code == 200

    async def test_on_publish_done_multiple_times(self, client, db_session):
        stream = StreamList(stream="multi_delete")
        db_session.add(stream)
        await db_session.commit()
        await client.post(
            "/stream_ending", data={"app": "live", "name": "multi_delete"}
        )
        await db_session.commit()
        response = await client.post(
            "/stream_ending", data={"app": "live", "name": "multi_delete"}
        )
        assert response.status_code == 200
