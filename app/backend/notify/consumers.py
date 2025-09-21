import json

from channels.generic.websocket import AsyncWebsocketConsumer


class OBSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "obs_group"
        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"echo": data}))

    async def obs_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))
