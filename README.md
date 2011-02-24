django-api
================




Installation
------------

Obtain django_api package and place it somewhere on your PYTHONPATH, for example
in your project directory (where settings.py is). 

Alternatively, if you are 
using some sort of virtual environment, like virtualenv, you can perform a 
regular installation or use [pip][]:
    
    python setup.py install

    # or ...

    pip install -e git://github.com/jpulgarin/django-api.git#egg=django-api

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
username and token parameter to the `token_new` view. 
Using curl, the request would look like:

    curl -d "username=jpulgarin&password=GGGGGG" http://www.yourdomain.com/token/new.json 

If the request is successful, you will receive a JSON response like so:

    {"success": true, "token": "2uy-420a8efff7f882afc20d", "user": 1}

### Verifying a Token

You can verify that a token matches a given user by

    



Acknowledgements
----------------

The token generating code is from `django.contrib.auth.tokens`, but modified so
that it does not hash on a user's last login.


