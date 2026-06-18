import pytest
from app.models.auth import StreamList
from sqlalchemy import select

pytestmark = pytest.mark.anyio


class TestGetListStreams:
    async def test_empty_list(self, client):
        response = await client.get("/get_list_streams")
        assert response.status_code == 200
        assert response.json() == []

    async def test_with_streams(self, client, db_session):
        streams = [
            StreamList(stream="stream_1"),
            StreamList(stream="stream_2"),
            StreamList(stream="stream_3"),
        ]
        db_session.add_all(streams)
        await db_session.commit()
        response = await client.get("/get_list_streams")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "stream_1" in data
        assert "stream_2" in data
        assert "stream_3" in data

    async def test_duplicate_streams(self, client, db_session):
        stream = StreamList(stream="duplicate_stream")
        db_session.add(stream)
        await db_session.commit()
        response = await client.get("/get_list_streams")
        assert response.status_code == 200
        data = response.json()
        assert data.count("duplicate_stream") == 1
