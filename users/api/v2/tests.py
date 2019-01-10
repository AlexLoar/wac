import json

from django.urls import reverse

from rest_framework.test import APITestCase


class ExampleTestCase(APITestCase):
    url = reverse('users_v2:api_v2_example')

    def test_valid_requests_success(self):
        response = self.client.get(self.url)

        expected_body = {'data': 'API v2 folder structure example'}
        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_body, json.loads(response.content))
