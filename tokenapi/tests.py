import json

from django.test import TestCase
from django.core.urlresolvers import reverse

try:
    from django.contrib.auth import get_user_model
except ImportError: # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from tokenapi.tokens import token_generator


class TokenManagementTestCase(TestCase):
    username = "jpulgarin"
    email = "jp@julianpulgarin.com"
    password = "GGGGGG"

    def setUp(self):
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()

        self.token = token_generator.make_token(self.user)

    def test_token_new_correct(self):
        response = self.client.post(reverse('api_token_new'), {
            'username': self.username,
            'password': self.password,
        })

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user'], self.user.pk)
        self.assertEqual(data['token'], self.token)

    def test_token_new_incorrect(self):
        credentials = ((
            self.username,
            "AAAAAA",
        ), (
            "j",
            self.password,
        ), (
            "j",
            "AAAAAA",
        ))

        for username, password in credentials:
            response = self.client.post(reverse('api_token_new'), {
                'username': username,
                'password': password,
            })

            data = json.loads(response.content)

            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['success'])
            self.assertTrue(data['errors'])
            self.assertNotEqual(data.get('user'), self.user.pk)
            self.assertNotEqual(data.get('token'), self.token)

    def test_token_correct(self):
        response = self.client.post(reverse('api_token', kwargs={'token': self.token, 'user': self.user.pk}))

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_token_incorrect(self):
        incorrect_token = self.token[::-1]

        response = self.client.post(reverse('api_token', kwargs={'token': incorrect_token, 'user': self.user.pk}))

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertTrue(data['errors'])
