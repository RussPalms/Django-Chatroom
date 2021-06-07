# using channels, we're able to access the django user authentication system
from channels.auth import AuthMiddlewareStack
# this is some mechanics from channels so that we can utilize routing
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# this is similar to using urlpatters, but for channel routing
# when we get a wsgi request, this is how to route it
application = ProtocolTypeRouter(
    {
        'websocket': AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
    }
)