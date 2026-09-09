from channels.testing import WebsocketCommunicator,ChannelsLiveServerTestCase
from chat_system.asgi import application
from globals.test_objects import create_chat_message,create_chat,create_user
import jwt
from django.conf import settings
from unittest.mock import patch

class TestChatWebSocket(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = create_user()
        self.room = create_chat(members=[self.user])
        self.token = jwt.encode(
            {'user_id': self.user.id},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

    def endpoint(self,access_token):
        return f'/ws/chat/{self.room.slug}/?token={access_token}'

    async def test_authenticated_user_can_connect(self):
        communicator = WebsocketCommunicator(
            application,
            self.endpoint(self.token)
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_unauthenticated_user_cannot_connection(self):
        communicator = WebsocketCommunicator(
            application,
            self.endpoint('')
        )
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        await communicator.disconnect() 

    @patch('chat.ws.consumers.send_offline_unread_notification.delay')
    async def test_valid_message(self,mock_task):
        communicator = WebsocketCommunicator(
            application,
            self.endpoint(self.token)
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.send_json_to({
            'action': 'send_message',
            'content': 'Hello'
        })
        response = await communicator.receive_json_from()
        print(response)
        self.assertEqual(response['content'], 'Hello')
        await communicator.disconnect()

    @patch('chat.ws.consumers.send_offline_unread_notification.delay')
    async def test_valid_message_is_broadcast_to_clients(self,moc_task):
        communicator_1 = WebsocketCommunicator(
            application,
            self.endpoint(self.token)
        )
        communicator_2 = WebsocketCommunicator(
            application,
            self.endpoint(self.token)
        )
        connected_1, _ = await communicator_1.connect()
        connected_2, _ = await communicator_2.connect()
        self.assertTrue(connected_1)
        self.assertTrue(connected_2)

        await communicator_1.send_json_to({
            'action': 'send_message',
            'content': 'Hello from test'
        })
        response_1 = await communicator_1.receive_json_from()
        response_2 = await communicator_2.receive_json_from()

        print(response_1)
        print(response_2)
        self.assertEqual(response_1['content'], 'Hello from test')
        self.assertEqual(response_2['content'], 'Hello from test')
        await communicator_1.disconnect()
        await communicator_2.disconnect()


    async def test_invalid_message(self):
        communicator = WebsocketCommunicator(
            application,
            self.endpoint(self.token)
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'action': 'send_message',
            'content': ''
        })
        response = await communicator.receive_json_from()
        print(response)
        self.assertEqual(response['error'], 'Invalid Message')
        await communicator.disconnect()