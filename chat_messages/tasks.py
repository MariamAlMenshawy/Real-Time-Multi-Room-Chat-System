from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from chat.models import ChatRoom
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Count


@shared_task
def send_offline_unread_notification(message_id):
    message = Message.objects.select_related('room','sender').get(id=message_id)
    room = message.room

    for user in room.members.all():
        if user.id == message.sender_id:        # هو اللي باغت الرسالة
            continue

        is_online = cache.get(f'user_online_{user.id}') # هنرجع كل اليوزر الاونلاين
        if not is_online and user.email:  # لو اليوزر مش اونلاين وعنده ايميل
            send_mail( subject=f'New message in {room.name}',
                message=(
                    f'You have a new unread message in {room.name}.\n\n'
                    f'From: {message.sender.username}\n'
                    f'Message: {message.content}'
                ),
                from_email='noreply@example.com',
                recipient_list=[user.email],
                fail_silently=False,
            )


@shared_task
def send_daily_activity_digest():
    rooms = ChatRoom.objects.annotate(total_messages=Count('message_set'))  # هنحسب عدد الرسائل لكل روم
    admins = User.objects.filter(is_staff=True,is_active=True).exclude(email='')

    for admin in admins:
        report = ''
        for room in rooms:
            report += f'{room.name}: {room.total_messages} messages\n'
            
        send_mail(
            subject='Daily Activity Digest',
            message=report,
            from_email='noreply@example.com',
            recipient_list=[admin.email],
            fail_silently=False,
        )