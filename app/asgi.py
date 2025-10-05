import os
import django
import asyncio

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from app.backend.notify.client import TwitchEventHandler
from app.backend.notify.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)


handler = TwitchEventHandler(channel_name="kirssei")
loop = asyncio.get_event_loop()
loop.create_task(handler.run_forever())
