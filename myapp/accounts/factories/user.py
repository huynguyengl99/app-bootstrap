import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "accounts.User"
        django_get_or_create = ("email",)

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
