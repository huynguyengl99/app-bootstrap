from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        await self.send_json(
            {
                "message": "hello",
            }
        )
