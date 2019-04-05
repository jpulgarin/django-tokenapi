from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from tokenapi.tokens import token_generator


class TokenBackend(ModelBackend):
    def authenticate(self, request=None, pk=None, token=None):
        try:
            user = get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return None

        # Reject users with is_active=False. Custom user models that don't have
        # that attribute are allowed.
        is_active = getattr(user, 'is_active', None)
        if (is_active or is_active is None) and token_generator.check_token(user, token):
            return user
