import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer


logger = logging.getLogger('websocket')


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = (
            self.scope['url_route']['kwargs']['room_name']
        )

        self.room_group_name = f'chat_{self.room_name}'

        self.user = self.scope.get('user')

        # ----------------------------------------------------
        # Authentication
        # ----------------------------------------------------

        if not self.user or self.user.is_anonymous:

            logger.warning(
                'Unauthenticated WebSocket rejected.'
            )

            await self.close()
            return

        # ----------------------------------------------------
        # Join Redis channel group
        # ----------------------------------------------------

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        logger.info(
            'User %s connected to room %s',
            self.user.username,
            self.room_name
        )

    async def disconnect(self, close_code):

     logger.info(
        'WebSocket disconnected. User=%s Room=%s CloseCode=%s',
        self.user.username
        if self.user and not self.user.is_anonymous
        else 'Anonymous',
        self.room_name,
        close_code
    )

     try:

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

     except Exception as e:

        logger.exception(
            'Error during WebSocket disconnect: %s',
            str(e)
        )

    async def receive(self, text_data):

        try:

            data = json.loads(text_data)

        except json.JSONDecodeError:

            await self.send(
                text_data=json.dumps({
                    'error': 'Invalid JSON.'
                })
            )

            return

        message = data.get('message')

        if not message:

            await self.send(
                text_data=json.dumps({
                    'error': 'Message is required.'
                })
            )

            return

        logger.info(
            'User %s sent message to room %s',
            self.user.username,
            self.room_name
        )

        # ----------------------------------------------------
        # Broadcast
        # ----------------------------------------------------

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                'message': event['message'],
                'username': event['username'],
            })
        )