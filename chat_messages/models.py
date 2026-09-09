from django.db import models
from chat.models import ChatRoom
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    