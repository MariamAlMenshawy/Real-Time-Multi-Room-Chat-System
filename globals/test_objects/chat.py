from chat.models import ChatRoom

def create_chat(
    name = 'Chat Room 1',
    slug = 'chat-room-slug',
    description = 'This is the description of chat room',
    is_private = False,
    members = None ,
):
    chat = ChatRoom.objects.create(
        name = name,
        slug = slug,
        description = description,
        is_private = is_private,
    )
    if members: 
        chat.members.set(members) 

    return chat



