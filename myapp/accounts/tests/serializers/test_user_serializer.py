from django.test import TestCase

from accounts.models import User
from accounts.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def test_user_data(self):
        email = "user@mail.com"
        user = User.objects.create_user(email, "p@ssw0rd")
        user_data = UserSerializer(user).data

        assert user_data == {
            "email": email,
            "is_admin": False,
        }
