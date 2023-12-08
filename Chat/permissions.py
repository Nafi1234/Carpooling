from rest_framework import permissions
from django.db.models import Q
from logging import getLogger

from .models import Chat


logger = getLogger('chat_permissions')


class HasChatPermissions(permissions.BasePermission):

    message = 'Chat does not exist'
    code = 404

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
        
            chat_uuid = view.kwargs.get('chat_uuid')
            Chat.objects.get(Q(uuid=chat_uuid),
                             (Q(user1=request.user) | Q(user2=request.user)))
            return True
        except Chat.DoesNotExist:
            logger.warning(
                f'Chat access permission denied for user {request.user}')
            return False
        except Exception:
            logger.exception('Error checking chat permission')