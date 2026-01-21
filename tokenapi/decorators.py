import binascii
from functools import wraps
from base64 import b64decode

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from tokenapi.http import JsonResponseBadRequest, JsonResponseForbidden, JsonResponseUnauthorized


def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        user = request.POST.get('user', request.GET.get('user'))
        token = request.POST.get('token', request.GET.get('token'))

        if not (user and token) and basic_auth:
            try:
                auth_method, auth_string = basic_auth.split(' ', 1)
            except ValueError:
                return JsonResponseBadRequest("Invalid Authorization header format.")

            if auth_method.lower() == 'basic':
                try:
                    auth_string = b64decode(auth_string.strip())
                    user, token = auth_string.decode().split(':', 1)
                except (binascii.Error, ValueError):
                    return JsonResponseBadRequest("Invalid Basic auth encoding.")

        if not (user and token):
            return JsonResponseUnauthorized("Must include 'user' and 'token' parameters with request.")

        user = authenticate(pk=user, token=token)
        if user:
            request.user = user
            return view_func(request, *args, **kwargs)

        return JsonResponseForbidden("Incorrect user and token pair.")
    return _wrapped_view
