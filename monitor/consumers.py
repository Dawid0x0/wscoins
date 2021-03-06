import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class MonitorConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'mcoins'

        # Join to group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    def send_prices(self, event):
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=data)
        