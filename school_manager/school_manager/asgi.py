"""
ASGI config for school_manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
import core.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_manager.settings')

from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": URLRouter(
        core.routing.websocket_urlpatterns
    ),
})

