from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^robot/(?P<room_name>[^/]+)/$', consumers.RobotConsumer),
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
