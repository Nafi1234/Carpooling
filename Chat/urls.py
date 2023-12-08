from django.urls import path
from .views import get_messages


urlpatterns = [
    path('get-messages/<int:sender_id>/<int:receiver_id>/', get_messages, name='get_messages'),

]