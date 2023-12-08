from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from user.models import User
from .models import Chat
from rest_framework.decorators import api_view
from .serializers import ChatSerializer
@api_view(['GET'])
def get_messages(request, sender_id, receiver_id):
    sender = get_object_or_404(User, id=sender_id)
    receiver = get_object_or_404(User, id=receiver_id)

    # Fetch chat messages from the database
    messages = Chat.objects.filter(
        (Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
    ).order_by("timestamp")
    print("giving the messages", messages)

    # Serialize messages to JSON with many=True
    serializer = ChatSerializer(messages, many=True)
    print(serializer.data)

    return Response(serializer.data)

