from django.urls import re_path

from tokenapi.views import token, token_new


urlpatterns = [
    re_path(r'^new.json$', token_new, name='api_token_new'),
    re_path(r'^(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
