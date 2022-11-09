import json
import time

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_live_feed()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def send_live_feed(self):
        feed = {
            'val': 100
        }
        for i in range(100):
            feed['val'] += i
            await self.send(text_data=json.dumps(feed))
            time.sleep(3)