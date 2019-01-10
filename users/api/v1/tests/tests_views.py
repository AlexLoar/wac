from django.urls import reverse
from users.models import CustomUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class LoginTestCase(APITestCase):
    url = reverse('users_v1:login')

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

    def test_authenticate_without_username(self):
        response = self.client.post(self.url, {'password': 'whatever'})
        self.assertEqual(400, response.status_code)

    def test_authenticate_without_password(self):
        response = self.client.post(self.url, {'username': 'whatever'})
        self.assertEqual(400, response.status_code)

    def test_authenticate_with_non_existent_user(self):
        response = self.client.post(self.url, {'username': 'foo', 'password': 'whatever'})
        self.assertEqual(400, response.status_code)
        self.assertIn(b'Invalid credentials', response.content)

    def test_authenticate_with_wrong_password(self):
        response = self.client.post(self.url, {'username': self.username, 'password': 'WRONG_PASSWORD'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid credentials', response.content)

    def test_authenticate_with_valid_data(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.content)


class CustomUserListTestCase(APITestCase):
    url = reverse('users_v1:list')

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = CustomUser.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.user_2 = CustomUser.objects.create_user("mary", "mary@earth.com", "super_secret")
        self.token_2 = Token.objects.create(user=self.user_2)

        self.response = self.client.get(self.url)

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_custom_users_returns_200(self):
        self.assertEqual(200, self.response.status_code)
        self.assertTrue(len(self.response.content), 2)

    def test_list_custom_users_without_login_returns_401(self):
        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertEqual(401, self.response.status_code)
        self.assertIn(b'Authentication credentials were not provided', self.response.content)


class CustomDetailTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = CustomUser.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.user_2 = CustomUser.objects.create_user("mary", "mary@earth.com", "super_secret")
        self.token_2 = Token.objects.create(user=self.user_2)

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_detail_custom_user_retrieve_its_user(self):
        response = self.client.get(reverse('users_v1:detail', kwargs={"pk": self.user.id}))
        self.assertEqual(200, response.status_code)

    def test_detail_custom_users_retrieves_not_own_user_returns_403(self):
        response = self.client.get(reverse('users_v1:detail', kwargs={"pk": self.user_2.id}))
        self.assertEqual(403, response.status_code)

    def test_detail_custom_users_without_login_returns_401(self):
        self.client.logout()
        self.response = self.client.get(reverse('users_v1:detail', kwargs={"pk": self.user_2.id}))
        self.assertEqual(401, self.response.status_code)
        self.assertIn(b'Authentication credentials were not provided', self.response.content)

    def test_update_not_its_own_user_returns_403(self):
        data = {
            "name": "Foo",
            "first_name": "Bar",
            "last_name": "FooBar",
            "email": "foo@bar.com"
        }
        response = self.client.put(reverse('users_v1:detail', kwargs={"pk": self.user_2.id}), data=data)
        self.assertEqual(403, response.status_code)

    def test_update_correct_user_returns_200(self):
        data = {
            "name": "Foo",
            "first_name": "Bar",
            "last_name": "FooBar",
            "email": "foo@bar.com"
        }
        response = self.client.put(reverse('users_v1:detail', kwargs={"pk": self.user.id}), data=data)
        self.assertEqual(200, response.status_code)
