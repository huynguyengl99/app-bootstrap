from channels.routing import URLRouter
from django.urls import path

from ws_app.routing import ws_app_urls

ws_nested_router = URLRouter([*ws_app_urls])

ws_routers = URLRouter(
    [
        path("ws/", ws_nested_router),
    ]
)
