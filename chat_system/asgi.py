import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_system.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from channels.security.websocket import AllowedHostsOriginValidator
from .ws_middleware import JWTAuthentication
from chat.ws.routing import ws_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthentication(
            URLRouter(ws_urls)
        )
    ),

})