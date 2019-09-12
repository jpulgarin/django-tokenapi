SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF = 'tests.urls'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'tokenapi.backends.TokenBackend',
)
