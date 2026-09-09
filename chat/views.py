from django.shortcuts import get_object_or_404, render
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from .mixins import CacheQuerysetMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.

# GET all active public rooms
class RoomList(CacheQuerysetMixin,ListAPIView):
    cache_key = 'all_rooms'
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.filter(is_private=False)


# GET room details
class Room_slug(RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        slug = self.kwargs['slug']
        cache_key = f'room_{slug}'
        room = cache.get(cache_key)

        if room is not None:
            print('✓ Cache HIT')
            return room
        
        print('X Cache MISS - fetching from DB')
        room = get_object_or_404(ChatRoom,slug=slug)
        cache.set(cache_key,room,timeout=60)
        return room


# POST new room
class PostRoom(CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('all_rooms')
        