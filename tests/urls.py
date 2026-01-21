from django.urls import include, re_path

from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse


@token_required
def test_view(request):
    return JsonResponse({'user_id': request.user.pk})


urlpatterns = [
    re_path(r'^token/', include('tokenapi.urls')),
    re_path(r'^test/$', test_view, name='test_view'),
]
