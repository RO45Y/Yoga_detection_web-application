import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PoseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("pose_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pose_group", self.channel_name)

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"message": "WebSocket connected"}))

    async def pose_update(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
