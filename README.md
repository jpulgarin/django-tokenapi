django-tokenapi
================

This is a Django application which allows you to create simple APIs
that use token-based authentication. You can easily open up existing views
to the API by adding a single decorator.

This is useful if you want to create applications on mobile devices which
connect to your Django website, but where only your clients are expected to
access the API.

If instead you are looking to open up an API to the public, you are better off
going with a framework with OAuth support, of which there exist some really
good [implementations](https://bitbucket.org/jespern/django-piston/wiki/Home).

Requirements
------------
* Django 1.9+
* Python 2.7+

Installation
------------

First obtain `tokenapi` package and place it somewhere on your `PYTHONPATH`, for example
in your project directory (where settings.py is).

Alternatively, if you are
using some sort of virtual environment, like [virtualenv][], you can perform a
regular installation or use [pip][]:

    python setup.py install

    # or ...

    pip install django-tokenapi

[virtualenv]: http://pypi.python.org/pypi/virtualenv
[pip]: http://pip.openplans.org/

Add `tokenapi` to your `INSTALLED_APPS`.

Ensure that `django.contrib.auth.backends.ModelBackend` is in your `AUTHENTICATION_BACKENDS`.

Add `tokenapi.backends.TokenBackend` to your `AUTHENTICATION_BACKENDS`.

Include `tokenapi.urls` in your `urls.py`. It will look something like this:

    urlpatterns = [
        url(r'^token/', include('tokenapi.urls')),
    ]

Configuration
-------------

You can change the number of days that a token is valid for by setting
`TOKEN_TIMEOUT_DAYS` in `settings.py`. The default is `7`.

Usage
-----

### Obtaining a Token

You can obtain a token for a specific user by sending a POST request with a
username and password parameter to the `api_token_new` view.
Using [curl][], the request would look like:

    curl -d "username=jpulgarin&password=GGGGGG" http://www.yourdomain.com/token/new.json

[curl]: http://curl.haxx.se/

If the request is successful, you will receive a JSON response like so:

    {"success": true, "token": "2uy-420a8efff7f882afc20d", "user": 1}

An invalid username and password pair will produce a response like so:

    {"success": false, "errors": "Unable to log you in, please try again"}

Note that if you User model has an `is_active` flag, the authentication logic will not allow inactive users to obtain or use tokens.

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
`tokenapi.decorators.token_required` decorator. There are also
JSON helper functions to make it easier to deal with JSON.
This is an example of an API compatible view:

    from tokenapi.decorators import token_required
    from tokenapi.http import JsonResponse, JsonError, JsonResponseBadRequest, JsonResponseUnauthorized, JsonResponseForbidden, JsonResponseNotFound, JsonResponseNotAllowed, JsonResponseNotAcceptable

    @token_required
    def index(request):
        if request.method == 'POST':
            data = {
                'test1': 49,
                'test2': 'awesome',
            }
            return JsonResponse(data)
        else:
            return JsonError("Only POST is allowed")

### Using a Token

#### Request Parameters

The client can access any API compatible view by sending a request to it,
and including `user` and `token` as request parameters (either GET or POST).
Accessing the example view above using curl might look like:

    curl -d "user=1&token=2uy-420a8efff7f882afc20d" http://www.yourdomain.com/new.json

You would receive the following response:

    {"success": true, "test1": 49, "test2": "awesome"}

#### Basic authentication


Alternately, you can access any API compatible view by including the user and token in
the Authorization header according to the
[basic access authentication](http://en.wikipedia.org/wiki/Basic_access_authentication)
scheme. To construct the Authorization header:

1. Combine user id and token into string "user:token"
2. Encode resulting string using Base64
3. Prepend "Basic " (including the trailing space) to the resulting Base64 encoded string

If, in the same request, you provide credentials via both request parameters and the
Authorization header, the request parameters will be used for authentication.

Acknowledgements
----------------

The token generating code is from `django.contrib.auth.tokens`, but modified so
that it does not hash on a user's last login.
