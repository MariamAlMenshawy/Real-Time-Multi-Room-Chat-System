from chat_messages.models import Message


def create_chat_message(
    room,
    sender,
    content='This is a content of message',
    is_read=False,
):
    return Message.objects.create(
        room=room,
        sender=sender,
        content=content,
        is_read=is_read,
    )

