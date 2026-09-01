import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'SkillSwap.settings'
)

from django.core.asgi import get_asgi_application

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

from django.urls import re_path

from .consumers import ChatConsumer
from .jwt_middleware import JWTAuthMiddleware


django_asgi_app = get_asgi_application()


websocket_urlpatterns = [

    re_path(
        r'^ws/chat/(?P<room_name>\w+)/$',
        ChatConsumer.as_asgi()
    ),

]


application = ProtocolTypeRouter({

    # --------------------------------------------------------
    # Normal HTTP requests
    # --------------------------------------------------------

    'http': django_asgi_app,

    # --------------------------------------------------------
    # JWT-authenticated WebSocket requests
    # --------------------------------------------------------

    'websocket': JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),

})