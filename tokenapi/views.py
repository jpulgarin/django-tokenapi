from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

try: 
    import simplejson as json
except ImportError: 
    import json

from tokenapi.tokens import token_generator
from tokenapi.http import JSONResponse, JSONError



# Creates a token if the correct username and password is given
# token/new.json
# Required: username&password
# Returns: success&token&user&username
@csrf_exempt
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
                }
                return JSONResponse(data)
            else:
                return JSONError("Unable to log you in, please try again")

# Checks if a given token and user pair is valid
# token/:token/:user.json
# Required: user
# Returns: success
def token(request, token, user):
    data = {}
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return JSONError("User does not exist.")
    if token_generator.check_token(user, 
        token): 
        data['success'] = True
    else:
        return JSONError("Token did not match user.")
    return JSONResponse(data)
