from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoCallConsumer(AsyncWebsocketConsumer):
    users = set()
    print('connect')

    async def connect(self):
        print('connect')
        await self.accept()
        VideoCallConsumer.users.add(self)


    async def disconnect(self, close_code):
        VideoCallConsumer.users.remove(self)
        print('connect')

    async def receive(self, text_data):
        data = json.loads(text_data)
        print('connect')

        if data["type"] == "join":
            for user in VideoCallConsumer.users:
                if user != self:
                    await user.send(json.dumps({"type": "offer", "peerId": data["peerId"]}))
        elif data["type"] in ["offer", "answer", "candidate"]:
            for user in VideoCallConsumer.users:
                if user != self:
                    await user.send(text_data)