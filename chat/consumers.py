# we want to create an application that's asynchronous
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    # this is going to change how the core behaves
    async def connect(self):
        # first we need to get the name of the chatroom
        # because we're using advanced routing this allows as to extract information from the route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # now we need to define the room group name
        self.room_group_name = 'chat_%s' % self.room_name

        # now construct a group
        # utilizing groups allows us to broadcast messages to those user inside the group
        await self.channel_layer.group_add(
            self.room_group_name,
            # the channel_name attribute contains a pointer to the channel layer instance and the 
            # channel name that will reach the consumer
            self.channel_name
        )

        await self.accept()

    #     # as soon as we connect, we're going to send a message to the group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             # we setup a group message to send
    #             # manage that
    #             # recieve the message from the group
    #             # send it accross via web sockets
    #             'type': 'tester_message',
    #             'tester': 'hello world',
    #         }
    #     )

    # async def tester_message(self, event):
    #     tester = event['tester']

    #     await self.send(text_data=json.dumps(
    #         {
    #             'tester': tester,
    #         }
    #     ))

    # here we're going to discard the group
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    pass