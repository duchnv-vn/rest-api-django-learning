from django.test import SimpleTestCase
# from app import calc
from rest_framework.test import APIClient


class TestViews(SimpleTestCase):
    client = APIClient()

    def test_get_greetings(self):
        pass
        # res = self.client.get('/greetings/')

        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.data, ['Hello', 'Ciao', 'Xin chao'])
