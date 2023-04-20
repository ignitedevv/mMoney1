import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    peers = set()

    async def connect(self):
        await self.accept()
        self.peers.add(self)

    async def disconnect(self, close_code):
        if hasattr(self, 'peer_id'):
            for peer in self.peers:
                if peer != self:
                    await peer.send(text_data=json.dumps({
                        'type': 'leave',
                        'peerId': self.peer_id,
                    }))
        self.peers.remove(self)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type == 'join':
            peer_id = data['peerId']
            self.peer_id = peer_id

            for peer in self.peers:
                if peer != self:
                    await peer.send(text_data=json.dumps({
                        'type': 'offer',
                        'peerId': peer_id,
                    }))