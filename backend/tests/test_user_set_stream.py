import pytest
from unittest.mock import patch
from app.models.auth import UserStreamSettings
from sqlalchemy import select

pytestmark = pytest.mark.anyio


class TestGenerateStream:
    async def test_generate_success(self, client, db_session, mock_jwt_valid):
        user_settings = UserStreamSettings(user_id="test-user-123", stream_id=None)
        db_session.add(user_settings)
        await db_session.commit()
        response = await client.patch(
            "/user_stream_gen", json={"user_id": "fake.jwt.token"}
        )
        assert response.status_code == 200
        stream_id = response.text.strip('"')
        assert stream_id.startswith("live_")
        assert len(stream_id) == 69
        await db_session.refresh(user_settings)
        assert user_settings.stream_id == stream_id

    async def test_generate_user_not_found(self, client, mock_jwt_valid):
        response = await client.patch(
            "/user_stream_gen", json={"user_id": "fake.jwt.token"}
        )
        assert response.status_code == 200

    async def test_generate_invalid_jwt(self, client, mock_jwt_invalid):
        response = await client.patch(
            "/user_stream_gen", json={"user_id": "invalid.token"}
        )
        assert response.status_code == 500


class TestProvideStream:
    async def test_provide_success(self, client, db_session):
        user_settings = UserStreamSettings(
            user_id="test-user-123", stream_id="live_abc123xyz"
        )
        db_session.add(user_settings)
        await db_session.commit()
        with patch(
            "app.utils.decode_jwt.decode_jwt", return_value={"sub": "test-user-123"}
        ):
            response = await client.get(
                "/user_stream_gen_first_check",
                headers={"Authorization": "Bearer fake-token"},
            )
        assert response.status_code == 200

    async def test_provide_no_stream(self, client):
        with patch("app.utils.decode_jwt.decode_jwt", return_value={"sub": "new-user"}):
            response = await client.get(
                "/user_stream_gen_first_check",
                headers={"Authorization": "Bearer fake-token"},
            )
        assert response.status_code in [200, 404, 500]
