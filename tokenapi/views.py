from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from tokenapi.tokens import token_generator
from tokenapi.http import JsonResponse, JsonResponseUnauthorized, JsonResponseForbidden, JsonResponseNotAllowed


@csrf_exempt
def token_new(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not getattr(user, 'is_active', True):
                    return JsonResponseForbidden("User account is disabled.")

                data = {
                    'token': token_generator.make_token(user),
                    'user': user.pk,
                }
                return JsonResponse(data)
            else:
                return JsonResponseUnauthorized("Unable to log you in, please try again.")
        else:
            return JsonResponseUnauthorized("Must include 'username' and 'password' as POST parameters.")
    else:
        return JsonResponseNotAllowed("Must access via a POST request.")


def token(request, token, user):
    if authenticate(pk=user, token=token) is not None:
        return JsonResponse({})
    else:
        return JsonResponseUnauthorized("Token did not match user.")
