DJANGO_APPS += ("django.contrib.sites",)

THIRD_PARTY_APPS += (
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
)

LOCAL_APPS += ("accounts",)

# Social account
SITE_ID = 1

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}
