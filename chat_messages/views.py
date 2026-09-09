from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from chat.models import ChatRoom
from django.core.cache import cache
from rest_framework.response import Response
from .permissions import IsRoomMember
# Create your views here.

class MessagePagination(PageNumberPagination):
    page_size = 10

class MessageList(ListAPIView):
    pagination_class = MessagePagination
    serializer_class = MessageSerializer
    permission_classes = [IsRoomMember]

    def list(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        room = get_object_or_404(ChatRoom,slug=slug)
        cache_key = f'room_{slug}_messages'
        cached = cache.get(cache_key)

        if cached is not None:
            print('✓ Cache HIT')
            messages = cached

        else:
            print('X Cache MISS - fetching from DB')
            messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
            serializer = MessageSerializer(messages,many=True)
            messages = serializer.data
            cache.set(cache_key,messages,timeout=60)

        page = self.paginate_queryset(messages)  #قسم الرسائل إلى صفحات وخد الصفحة المطلوبة
        if page is not None:
            return self.get_paginated_response(page) #pagination رجع الصفحة ومعاها معلومات ال      

        return Response(messages) 