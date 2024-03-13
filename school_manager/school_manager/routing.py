from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path("chat/", include("core.routing")),
    ]),
})