from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150,unique=True)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User,related_name='chat_rooms')
