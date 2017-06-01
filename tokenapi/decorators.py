from functools import wraps
from base64 import b64decode

from tokenapi.http import JsonError, JsonResponseUnauthorized
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = None
        token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        user = request.POST.get('user', request.GET.get('user'))
        token = request.POST.get('token', request.GET.get('token'))

        if not (user and token) and basic_auth:
            auth_method, auth_string = basic_auth.split(' ', 1)

            if auth_method.lower() == 'basic':
                auth_string = b64decode(auth_string.strip())
                user, token = auth_string.decode().split(':', 1)

        if not (user and token):
            return JsonError("Must include 'user' and 'token' parameters with request.")

        user = authenticate(pk=user, token=token)
        if user:
            request.user = user
            return view_func(request, *args, **kwargs)

        return JsonResponseUnauthorized("You are unauthorized to view this page.")
    return _wrapped_view
