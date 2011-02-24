from django.conf.urls.defaults import *

urlpatterns = patterns('django_api.views',
    url(r'^token/new.json$', 'token_new', name="api_token_new"),
    url(r'^token/(?P<token>.{24}).json$', 'token', name="api_token"),
)
