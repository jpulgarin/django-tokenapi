from django.conf.urls import include, url

urlpatterns = [
    url(r'^token/', include('tokenapi.urls')),
]
