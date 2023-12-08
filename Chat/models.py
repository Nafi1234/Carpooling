from django.db import models
import uuid
from publishride.models import ReuquestRide
from user.models import User 
from django.core.validators import MinLengthValidator
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='user1_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='user2_chats', on_delete=models.CASCADE)
    content=models.TextField(null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Chat between {self.sender} and {self.receiver}"
    class Meta:
        ordering=['timestamp']
        verbose_name_plural="Message"
  