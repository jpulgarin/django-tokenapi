from django.contrib.auth.backends import ModelBackend
from tokenapi.tokens import token_generator
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
except ImportError: # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class TokenBackend(ModelBackend):
    def authenticate(self, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

        TOKEN_CHECK_ACTIVE_USER = getattr(settings, "TOKEN_CHECK_ACTIVE_USER", False)

        if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
            return None

        if token_generator.check_token(user,
            token):
            return user
        return None
