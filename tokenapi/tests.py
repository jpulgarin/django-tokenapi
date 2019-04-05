import json

from django.test import TestCase
from django.contrib.auth import get_user_model

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy

from tokenapi.tokens import token_generator


class DjangoTokenApiTestCase(TestCase):
    username = "jpulgarin"
    password = "GGGGGG"

    def setUp(self):
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.user.save()

        self.token = token_generator.make_token(self.user)

    def test_token_new(self):
        response = self.client.post(reverse('api_token_new'), {
            'username': self.username,
            'password': self.password,
        })

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user'], self.user.pk)
        self.assertEqual(data['token'], self.token)

    def test_token_new_get(self):
        response = self.client.get(reverse('api_token_new'), {
            'username': self.username,
            'password': self.password,
        })

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertNotIn('user', data)
        self.assertNotIn('token', data)


    def test_token_new_inactive_user(self):
        if hasattr(self.user, 'is_active'):
            self.user.is_active = False
            self.user.save()

            response = self.client.post(reverse('api_token_new'), {
                'username': self.username,
                'password': self.password,
            })

            data = json.loads(response.content.decode())

            # A 401 is returned if the authenticate call checks the is_active flag.
            # a 403 is returned if we detect is_active=False after authentication
            # succeeds.
            self.assertIn(response.status_code, (401, 403))
            self.assertFalse(data['success'])
            self.assertIn('errors', data)
            self.assertNotIn('user', data)
            self.assertNotIn('token', data)

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

            data = json.loads(response.content.decode())

            self.assertEqual(response.status_code, 401)
            self.assertFalse(data['success'])
            self.assertIn('errors', data)
            self.assertNotIn('user', data)
            self.assertNotIn('token', data)

    def test_token(self):
        response = self.client.post(reverse('api_token', kwargs={'token': self.token, 'user': self.user.pk}))

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_token_non_existent_user(self):
        response = self.client.post(reverse('api_token', kwargs={'token': self.token, 'user': self.user.pk + 1}))

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)

    def test_token_incorrect_token(self):
        incorrect_token = self.token[::-1]

        response = self.client.post(reverse('api_token', kwargs={'token': incorrect_token, 'user': self.user.pk}))

        data = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)

    def test_token_inactive_user(self):
        if hasattr(self.user, 'is_active'):
            self.user.is_active = False
            self.user.save()

            response = self.client.post(reverse('api_token', kwargs={'token': self.token, 'user': self.user.pk}))

            data = json.loads(response.content.decode())

            self.assertEqual(response.status_code, 401)
            self.assertFalse(data['success'])
            self.assertIn('errors', data)
