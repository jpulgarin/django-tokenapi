from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    # GET API
    (r'^token/(?P<token>.{24}).json$', 'token'),
    (r'^points.json$', 'points'),

    # POST API
    (r'^token/new.json$', 'token_new'),
    (r'^signup.json$', 'signup'),
    (r'^transaction/new.json$', 'transaction_new'),
    (r'^redemption/new.json$', 'redemption_new'),
)
