"""
ASGI config for ctef project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctef.settings")

asgi_application = get_asgi_application()

from ctef_core.routing import websocket_urlpatterns
from . import urls

# Add the websocket url patterns from the containers
websocket_urlpatterns = websocket_urlpatterns + urls.wspatterns
print(websocket_urlpatterns)

# TODO: Adapt this to forward websocket connections to container proxy as well
# https://channels.readthedocs.io/en/latest/topics/routing.html#
application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
