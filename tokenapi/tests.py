import json

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from tokenapi.tokens import token_generator

class TokenManagementTestCase(TestCase):

    username = "jpulgarin"
    email = "jp@julianpulgarin.com"
    password = "GGGGGG"

    # inactive user
    inactive_username = "jpulgarin2"
    inactive_email = "jp2@julianpulgarin.com"
    inactive_password = "HHHHHH"

    def setUp(self):
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.token = token_generator.make_token(self.user)

        self.inactive_user = User.objects.create_user(self.inactive_username, self.inactive_email, self.inactive_password)
        self.inactive_user.is_active = False
        self.inactive_user.save()
        self.inactive_token = self._get_inactive_token()

    @override_settings(TOKEN_CHECK_ACTIVE_USER=False)
    def _get_inactive_token(self):
        return token_generator.make_token(self.inactive_user)


    @override_settings(TOKEN_CHECK_ACTIVE_USER=True)
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

    @override_settings(TOKEN_CHECK_ACTIVE_USER=False)
    def test_token_new_inactive_correct(self):
        response = self.client.post(reverse('api_token_new'), {
            'username': self.inactive_username,
            'password': self.inactive_password,
        })

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user'], self.inactive_user.pk)
        self.assertEqual(data['token'], self.inactive_token)

    @override_settings(TOKEN_CHECK_ACTIVE_USER=True)
    def test_token_new_incorrect(self):
        credentials = ((
            self.username,
            "AAAAAA",
            401 # expected status
        ), (
            "j",
            self.password,
            401,
        ), (
            "j",
            "AAAAAA",
            401,
        ), (
            "jpulgarin2", # inactive user
            "HHHHHH",
            403,
        ))

        for username, password, expected_response in credentials:
            response = self.client.post(reverse('api_token_new'), {
                'username': username,
                'password': password,
            })

            data = json.loads(response.content)

            self.assertEqual(response.status_code, expected_response)
            self.assertFalse(data['success'])
            self.assertTrue(data['errors'])

            self.assertNotEqual(data.get('user'), self.user.pk)
            self.assertNotEqual(data.get('token'), self.token)
            self.assertNotEqual(data.get('user'), self.inactive_user.pk)

    


    def test_token_correct(self):
        response = self.client.post(reverse('api_token', kwargs={'token': self.token, 'user': self.user.pk}))

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_token_incorrect(self):
        incorrect_token = self.token[::-1]

        response = self.client.post(reverse('api_token', kwargs={'token': incorrect_token, 'user': self.user.pk}))

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertTrue(data['errors'])
