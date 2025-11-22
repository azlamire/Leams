# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.auth_github_post200_response import AuthGithubPost200Response  # noqa: F401
from openapi_server.models.code import Code  # noqa: F401
from openapi_server.models.register_post200_response import RegisterPost200Response  # noqa: F401


def test_auth_github_post(client: TestClient):
    """Test case for auth_github_post

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/github".format(client_id='client_id_example', redierect_uri='redierect_uri_example', response_type=openapi_server.Code(), scope=['scope_example']),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_register_post(client: TestClient):
    """Test case for register_post

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/register",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_main_videos_categories_get(client: TestClient):
    """Test case for main_videos_categories_get

    
    """

    headers = {
        "authorization": 'authorization_example',
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/main/videos/categories",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

