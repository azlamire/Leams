# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.auth_github_post200_response import AuthGithubPost200Response
from openapi_server.models.code import Code
from openapi_server.models.register_post200_response import RegisterPost200Response


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def auth_github_post(
        self,
        client_id: Annotated[StrictStr, Field(description="Client Id of github")],
        redierect_uri: Annotated[StrictStr, Field(description="Where user will redierected")],
        response_type: Annotated[Code, Field(description="What type of response will be got")],
        scope: Annotated[List[StrictStr], Field(description="Which permissions will be granted to user")],
    ) -> AuthGithubPost200Response:
        """API for generating and sending GitHub token to sign via this one"""
        ...


    async def register_post(
        self,
    ) -> RegisterPost200Response:
        """API for creating new user and after logging it after this"""
        ...


    async def main_videos_categories_get(
        self,
        authorization: Annotated[StrictStr, Field(description="value must be `Bearer <token>` where `<token>` is api key prefixed with cal_")],
    ) -> None:
        """Getting from backend(S3) videos via recommendations"""
        ...
