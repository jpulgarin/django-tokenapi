from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

try: 
    import simplejson as json
except ImportError: 
    import json

from django_api.tokens import token_generator


# JSON helper functions
def JSONResponse(data, dump=True):
    return HttpResponse(
        json.dumps(data) if dump else data,
        mimetype='application/json',
    )

def JSONError(error_string):
    data = {
        'success': False,
        'errors': error_string,
    }
    return JSONResponse(data)


# Checks if a given token and user pair is valid
# token/:token.json
# Required: user
# Returns: success
def token(request, token):
    if 'user' in request.GET:
        data = {}

        try:
            user = User.objects.get(pk=request.GET['user'])
        except User.DoesNotExist:
            return JSONError("User does not exist.")
        if token_generator.check_token(user, 
            token): 
            data['success'] = True
        else:
            return JSONError("Token did not match user.")
        return JSONResponse(data)


# Creates a token if the correct username and password is given
# token_new.json
# Required: username&password
# Returns: success&token&user&username
def token_new(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            user = authenticate(username=request.POST['username'], 
                password=request.POST['password'])
            if user:
                data = {
                    'success': True,
                    'token': token_generator.make_token(user),
                    'user': user.pk,
                    'username': user.username,
                }
                return JSONResponse(data)
            else:
                return JSONError("Unable to log you in, please try again")
