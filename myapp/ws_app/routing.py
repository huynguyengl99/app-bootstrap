from django.urls import path

from ws_app.consumers import ChatConsumer

ws_app_urls = [
    path("greeting/", ChatConsumer.as_asgi()),
]
