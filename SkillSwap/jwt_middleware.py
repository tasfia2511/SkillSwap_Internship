import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token):

    try:
        access_token = AccessToken(token)

        user_id = access_token["user_id"]

        User = get_user_model()

        user = User.objects.get(
            id=user_id
        )

        logger.info(
            "JWT WebSocket authentication successful for user: %s",
            user.username
        )

        return user

    except Exception as e:

        logger.error(
            "JWT WebSocket authentication failed: %s",
            str(e)
        )

        return AnonymousUser()


class JWTAuthMiddleware:

    def __init__(self, app):

        self.app = app

    async def __call__(
        self,
        scope,
        receive,
        send
    ):

        query_string = (
            scope.get(
                "query_string",
                b""
            )
            .decode()
        )

        query_params = parse_qs(
            query_string
        )

        token = query_params.get(
            "token",
            [None]
        )[0]

        if token:

            scope["user"] = (
                await get_user_from_token(
                    token
                )
            )

        else:

            logger.warning(
                "WebSocket connection attempted without JWT token."
            )

            scope["user"] = AnonymousUser()

        return await self.app(
            scope,
            receive,
            send
        )