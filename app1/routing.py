from django.urls import path
from app1.consumers import PoseConsumer

websocket_urlpatterns = [path("ws/pose/", PoseConsumer.as_asgi())]
