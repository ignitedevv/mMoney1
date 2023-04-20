from django.urls import path
from budget import consumers

websocket_urlpatterns = [
    path("/budget/video_call/", consumers.VideoCallConsumer.as_asgi()),
]