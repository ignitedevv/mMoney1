import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive a message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender')
        offer = text_data_json.get('offer')
        answer = text_data_json.get('answer')
        ice_candidate = text_data_json.get('ice_candidate')

        if message and sender:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                }
            )
        elif offer:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': offer,
                }
            )
        elif answer:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': answer,
                }
            )
        elif ice_candidate:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_ice_candidate',
                    'ice_candidate': ice_candidate,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    # Receive WebRTC offer from room group
    async def webrtc_offer(self, event):
        offer = event['offer']

        # Send offer to WebSocket
        await self.send(text_data=json.dumps({
            'offer': offer,
        }))

    # Receive WebRTC answer from room group
    async def webrtc_answer(self, event):
        answer = event['answer']

        # Send answer to WebSocket
        await self.send(text_data=json.dumps({
            'answer': answer,
        }))

    # Receive WebRTC ICE candidate from room group
    async def webrtc_ice_candidate(self, event):
        ice_candidate = event['ice_candidate']

        # Send ICE candidate to WebSocket
        await self.send(text_data=json.dumps({
            'ice_candidate': ice_candidate,
        }))
