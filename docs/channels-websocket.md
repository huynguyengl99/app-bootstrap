# Django Channels (Websockets)

## 1. Intro

[Django Channels](https://channels.readthedocs.io/en/latest/) is a project that takes
Django and extends its abilities beyond HTTP - to handle WebSockets, chat protocols, 
IoT protocols, and more. It’s built on a Python specification called ASGI.

## 2. Running Locally
We add [Daphne](https://github.com/django/daphne) as a Django app so that we can
extend the normal runserver command to handle websocket connection.

```shell
bin/manage.sh runserver 8000
```

## 3. Deploy production
To have better deployment on production, we use [Gunicorn](https://docs.gunicorn.org/en/stable/index.html)
to handle and manager worker life circle. In order to use websocket with Gunicorn, we
need to use UvicornWorker as Gunicorn worker, for example the deploying command would be:

```shell
gunicorn config.asgi --chdir myapp --log-file - -k uvicorn.workers.UvicornWorker
```

More information about choosing webserver for asgi:
- https://asgi.readthedocs.io/en/latest/implementations.html#servers


## 4. Routing and Adding More WebSockets in Django Channels
Routing in Django Channels is similar to Django's URL routing. You can define WebSocket
routes in your [ws_app/routing.py](../myapp/ws_app/routing.py) file. You also can create
new app for grouping websocket business flow, but try to prefix with `ws_` to distinguish
between normal `http` and `websocket` connection. 

## 5. Asynchronous and Synchronous Operations with Database Access
### a. Intro
Django Channels allows you to write consumers either in synchronous or asynchronous style.
However, Django's ORM (Object-Relational Mapping) is not natively asynchronous. This means
you can't directly use Django's ORM (which interfaces with your database) within an async
consumer or async function.

Take a look on this https://docs.djangoproject.com/en/4.2/topics/async/ for more detail.
Below are some guidelines:

- When to use Async:
  - Use async when handling operations that can run concurrently and are I/O-bound, such as
  handling HTTP requests, WebSocket connections, and other network-related tasks. Normally,
  almost all of your consumer code should be written in `async` mode.
  - For instance, if you're building a chat application, handling each client's WebSocket
  connection in a separate async task allows you to serve multiple clients simultaneously.

- When to use Sync:
  - Use synchronous code for CPU-bound operations and whenever you interact with Django's ORM
  or other parts of Django that aren't async-safe. That includes most database-related
  operations and Django's middleware. Normally, all of your `rest views` should be written in
  sync mode.
  - For example, `celery` currently does not support `async` so you should write the code in
  `sync` mode. The same rules for https://www.django-rest-framework.org/ (API Views). 

### b. Converting between mode
You have two primary tools to convert between async and sync contexts:

- `asgiref.sync.async_to_sync`:

This decorator/function is used to call async functions from a synchronous context.

Example:

```python
from asgiref.sync import async_to_sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        async_to_sync(self.send)({
            "type": "websocket.accept",
        })
```

- `asgiref.sync.async_to_sync`:

`asgiref.sync.sync_to_async` or `channels.db.database_sync_to_async`: These decorators are used to call synchronous functions from an async context. The latter is specifically designed for database operations.

Example:

```python
from channels.db import database_sync_to_async
from my_custom_app.models import MyModel

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        instance = await self.get_instance_from_db(1)  # Fetch instance with id 1

    @database_sync_to_async
    def get_instance_from_db(self, id):
        return MyModel.objects.get(id=id)
```

Remember, always ensure that the Django ORM and other non-async-safe parts of Django are accessed in a synchronous context to prevent unexpected behavior.
