import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        await self.accept()
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "hello world"
        }))
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.send({
            "type": "websocket.send",
            "text": "room made"
        })

    async def websocket_receive(self, event):
        data_to_get = json.loads(event['text'])
        self.room_group_name = 'test_consumer_group'
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "value": json.dumps(data_to_get)
            }
        )

    async def websocket_disconnect(self, event):
        pass

    async def send_notification(self, event):
        print("sending notificationssss")
        await self.send(json.dumps({
            "type": "websocket.send",
            "data": event,
        }))
