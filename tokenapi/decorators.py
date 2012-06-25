from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python 2.4 fallback

def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.REQUEST.get('user')
        token = request.REQUEST.get('token')

        if user and token:
            user = authenticate(pk=user, token=token)
            if user:
                login(request, user)
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view
