from django.conf.urls import url

from tokenapi.views import token, token_new


urlpatterns = [
    url(r'^new.json$', token_new, name='api_token_new'),
    url(r'^(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
