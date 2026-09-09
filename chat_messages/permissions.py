from rest_framework.permissions import BasePermission

class IsRoomMember(BasePermission):

    def has_permission(self, request, view):
        slug = view.kwargs.get('slug')
        return request.user.is_authenticated and request.user.chat_rooms.filter(slug=slug).exists()