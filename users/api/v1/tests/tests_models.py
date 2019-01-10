from django.core import exceptions
from users.models import CustomUser

from rest_framework.test import APITestCase


class CustomUserModelTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "Batman"
        cls.email = "batman@batdomain.com"
        cls.password = "my_bat_password"
        cls.user = CustomUser.objects.create_user(cls.username, cls.email, cls.password)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_server_repr(self):
        expected_repr = f'{self.user}'

        self.assertEqual(expected_repr, str(self.user))

    def test_name_unicode_validation(self):
        with self.assertRaises(exceptions.ValidationError):
            user = CustomUser.objects.create_user('Wrong_?',
                                                  'mail@mail.com',
                                                  'qweKJrty12SDF3')
            user.full_clean()
