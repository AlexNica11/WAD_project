from django.urls import re_path
from StudentHub.consumers import ChatConsumer

websocket_urlpatterns = [
    # path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/(?P<slug>\w+)/chat/(?P<id>\w+)/$", ChatConsumer.as_asgi()),
    # '<slug:slug>/chat/<int:id>/'

]