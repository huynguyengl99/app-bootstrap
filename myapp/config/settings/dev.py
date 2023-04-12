from .base import *  # NOQA

DEBUG = True

INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
    "rest_framework.renderers.BrowsableAPIRenderer",
)

INTERNAL_IPS = ["127.0.0.1"]
