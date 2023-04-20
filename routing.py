from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from budget import consumers
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            [
                path("ws/budget/video_call/", consumers.VideoCallConsumer.as_asgi()),
            ]
        ),
    }
)