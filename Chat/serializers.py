from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError
from logging import getLogger

from .models import  Chat
from user.serializer import UserDetailsSerializer
from user.models import User
from publishride.serializers import UserSerializer

class ChatSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="receiver", read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'user_detail']