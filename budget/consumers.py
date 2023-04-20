import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    users = set()

    async def connect(self):
        await self.accept()
        VideoCallConsumer.users.add(self)

    async def disconnect(self, close_code):
        VideoCallConsumer.users.remove(self)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "join":
            for user in VideoCallConsumer.users:
                if user != self:
                    await user.send(json.dumps({"type": "offer", "peerId": data["peerId"]}))