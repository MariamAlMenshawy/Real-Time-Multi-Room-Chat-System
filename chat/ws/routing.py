from .consumers import ChatConsumer
from django.urls import path

ws_urls = [
    path('ws/chat/<slug:room_slug>/',ChatConsumer.as_asgi()),
]