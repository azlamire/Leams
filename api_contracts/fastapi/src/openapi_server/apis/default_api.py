# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.auth_github_post200_response import AuthGithubPost200Response
from openapi_server.models.code import Code
from openapi_server.models.register_post200_response import RegisterPost200Response


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth/github",
    responses={
        200: {"model": AuthGithubPost200Response, "description": "OK"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def auth_github_post(
    client_id: Annotated[StrictStr, Field(description="Client Id of github")] = Path(..., description="Client Id of github"),
    redierect_uri: Annotated[StrictStr, Field(description="Where user will redierected")] = Path(..., description="Where user will redierected"),
    response_type: Annotated[Code, Field(description="What type of response will be got")] = Path(..., description="What type of response will be got"),
    scope: Annotated[List[StrictStr], Field(description="Which permissions will be granted to user")] = Path(..., description="Which permissions will be granted to user"),
) -> AuthGithubPost200Response:
    """API for generating and sending GitHub token to sign via this one"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().auth_github_post(client_id, redierect_uri, response_type, scope)


@router.post(
    "/register",
    responses={
        200: {"model": RegisterPost200Response, "description": "OK"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def register_post(
) -> RegisterPost200Response:
    """API for creating new user and after logging it after this"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().register_post()


@router.get(
    "/main/videos/categories",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def main_videos_categories_get(
    authorization: Annotated[StrictStr, Field(description="value must be `Bearer <token>` where `<token>` is api key prefixed with cal_")] = Header(None, description="value must be &#x60;Bearer &lt;token&gt;&#x60; where &#x60;&lt;token&gt;&#x60; is api key prefixed with cal_"),
) -> None:
    """Getting from backend(S3) videos via recommendations"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().main_videos_categories_get(authorization)
