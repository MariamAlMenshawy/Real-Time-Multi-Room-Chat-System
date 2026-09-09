from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from django.core.cache import cache
from chat_messages.models import Message
from chat.models import ChatRoom
from chat_messages.serializers import MessageSerializer
from chat_messages.tasks import send_offline_unread_notification

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.GROUP_NAME = f'chat_{self.room_slug}'

        if self.user.is_authenticated:
            cache.set(f'user_online_{self.user.id}',True,timeout=300) # عشان نعرف مين الاونلاين
            async_to_sync(self.channel_layer.group_add)(
                self.GROUP_NAME,
                self.channel_name
            )
            self.accept()
        else:
            self.close()


    def disconnect(self, code):
        cache.delete(f'user_online_{self.user.id}') 
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME,
            self.channel_name
        )

    def receive(self, text_data = None, bytes_data = None):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'send_message':
            self.send_message(data)

        elif action == 'typing':
            self.typing(data)


    def send_message(self, data):
        content = data.get('content', '').strip()
        if not content or len(content)>1000:  #validate
            self.send(text_data=json.dumps({
                'error': 'Invalid Message'
            }))
            return
        
        room = ChatRoom.objects.get(slug=self.room_slug)
        message_data = {
            'room' : room.id,
            'sender' : self.user.id,
            'content' : content,
            'is_read' : False
        }
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            send_offline_unread_notification.delay(message.id)
        else:
            print(serializer.errors)
            return 
        cache_key = f'room_{self.room_slug}_messages'
        messages = cache.get(cache_key)
        if messages is not None:
            messages.insert(0, MessageSerializer(message).data)
            cache.set(cache_key, messages[:50], timeout=60)

        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
            }
        )


    def chat_message(self, message):
        self.send(text_data=json.dumps({
            'sender': message['sender'],
            'content': message['content'],
            'timestamp': message['timestamp'],
        }))

    def typing(self,data):
        is_typing = data.get('is_typing',True)
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                'type': 'typing_message',
                'sender': self.user.username,
                'is_typing': is_typing,
            }
        )

    def typing_message(self, message):
        self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': message['sender'],
            'is_typing': message['is_typing'],
        }))