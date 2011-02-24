django-api
================

This is a Django application which provides all you need to create a
[REST API](http://en.wikipedia.org/wiki/Representational_State_Transfer)
that uses token-based authentication.

This is useful if you want to create applications on mobile devices which
connect to your Django website, but where only your clients are expected to
access the API.

If instead you are looking to open up an API to the public, you are better off
going with [OAuth](http://oauth.net/) of which there exist some really good 
Django [implementations](https://github.com/simplegeo/python-oauth2).

Installation
------------

Obtain django_api package and place it somewhere on your PYTHONPATH, for example
in your project directory (where settings.py is). 

Alternatively, if you are 
using some sort of virtual environment, like [virtualenv][], you can perform a 
regular installation or use [pip][]:
    
    python setup.py install

    # or ...

    pip install -e git://github.com/jpulgarin/django-api.git#egg=django-api

[virtualenv]: http://pypi.python.org/pypi/virtualenv
[pip]: http://pip.openplans.org/

Add `django_api` to your `INSTALLED_APPS`.

Add `django_api.backends.TokenBackend` to your `AUTHENTICATION_BACKENDS`.

Include `django_api.urls` in your `urls.py`. It will look something like this:

    urlpatterns = patterns('',
        (r'', include('django_api.urls')),
    )


Configuration
-------------

You can change the number of days that a token is valid for by setting 
`TOKEN_TIMEOUT_DAYS` in `settings.py`. The default is `7`.


Usage
-----

### Obtaining a Token

You can obtain a token for a specific user by sending a POST request with a
username and token parameter to the `api_token_new` view. 
Using [curl][], the request would look like:

    curl -d "username=jpulgarin&password=GGGGGG" http://www.yourdomain.com/token/new.json 

[curl]: http://curl.haxx.se/

If the request is successful, you will receive a JSON response like so:

    {"success": true, "token": "2uy-420a8efff7f882afc20d", "user": 1}

An invalid username and password pair will produce a response like so:

    {"success": false, "errors": "Unable to log you in, please try again"}

You should store the `user` and `token` that are returned on the client 
accessing the API, as all subsequent calls will require that the request have 
a valid token and user pair.

### Verifying a Token

You can verify that a token matches a given user by sending a GET request
to the `api_token` view, and sending the token and user as part of the URL. 
Using curl it would look like:

    curl http://www.yourdomain.com/token/2uy-420a8efff7f882afc20d/1.json 

If valid, you will receive the following JSON response:

    {"success": true}

### Writing API Compatible Views

To allow a view to be accessed through token-based auth, use the 
`django_api.decorators.token_required` decorator. There are also 
JSON helper functions to make it easier to deal with JSON. 
This is an example of an API compatible view:

    from django_api.decorators import token_required
    from django api.views import JSONResponse, JSONError

    @token_required
    def index(request):
        if request.method == 'POST':
            data = {
                'success': True,
                'test1': 49,
                'test2': 'awesome',
            }
            return JSONResponse(data)
        else:
            return JSONError("Only POST is allowed")

### Using a Token

The client can access any API compatible view by sending a request to it, 
and including `user` and `token` as request parameters (either GET or POST).
Accessing the example view above using curl might look like:

    curl -d "user=1&token=2uy-420a8efff7f882afc20d" http://www.yourdomain.com/index.json

You would receive the following response:

    {"success": true, "test1": 49, "test2": "awesome"}


Acknowledgements
----------------

The token generating code is from `django.contrib.auth.tokens`, but modified so
that it does not hash on a user's last login.


