from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('stories/notification_testing/', consumers.NotificationConsumer.as_asgi())
]


