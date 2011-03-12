from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

try: 
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python 2.4 fallback

# Decorator which ensures the user has provided
# a correct user and token pair
def token_required(view_func):
    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'token' in request.REQUEST and \
            'user' in request.REQUEST:
                user = authenticate(pk=request.REQUEST['user'], token=request.REQUEST['token'])
                if user:
                    login(request, user)
                    return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _wrapped_view
