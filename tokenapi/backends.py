from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from tokenapi.tokens import token_generator


class TokenBackend(ModelBackend):
    def authenticate(self, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        if token_generator.check_token(user, 
            token): 
            return user
        return None
