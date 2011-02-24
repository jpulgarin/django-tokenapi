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

You can obtain a token for a specific user by sending a POST request t

Acknowledgements
----------------

The token generating code is from `django.contrib.auth.tokens`, but modified so
that it does not hash on a user's last login.


