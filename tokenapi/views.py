from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
except ImportError: # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from tokenapi.tokens import token_generator
from tokenapi.http import JsonResponse, JsonError, JsonResponseForbidden, JsonResponseUnauthorized


# Creates a token if the correct username and password is given
# token/new.json
# Required: username&password
# Returns: success&token&user
@csrf_exempt
def token_new(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                TOKEN_CHECK_ACTIVE_USER = getattr(settings, "TOKEN_CHECK_ACTIVE_USER", False)

                if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
                    return JsonResponseForbidden("User account is disabled.")

                data = {
                    'token': token_generator.make_token(user),
                    'user': user.pk,
                }
                return JsonResponse(data)
            else:
                return JsonResponseUnauthorized("Unable to log you in, please try again.")
        else:
            return JsonError("Must include 'username' and 'password' as POST parameters.")
    else:
        return JsonError("Must access via a POST request.")

# Checks if a given token and user pair is valid
# token/:token/:user.json
# Required: user
# Returns: success
def token(request, token, user):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return JsonError("User does not exist.")

    TOKEN_CHECK_ACTIVE_USER = getattr(settings, "TOKEN_CHECK_ACTIVE_USER", False)

    if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
        return JsonError("User account is disabled.")

    if token_generator.check_token(user, token):
        return JsonResponse({})
    else:
        return JsonError("Token did not match user.")
