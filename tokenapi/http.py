"""JSON helper functions"""
try:
    import simplejson as json
except ImportError:
    import json

from django.http import HttpResponse


def JsonResponse(data, dump=True, status=200):
    try:
        data['errors']
    except KeyError:
        data['success'] = True
    except TypeError:
        pass

    return HttpResponse(
        json.dumps(data) if dump else data,
        content_type='application/json',
        status=status,
    )


def JsonError(error_string, status=200):
    data = {
        'success': False,
        'errors': error_string,
    }
    return JSONResponse(data)


def JsonResponseBadRequest(error_string):
    return JsonError(error_string, status=400)


def JsonResponseUnauthorized(error_string):
    return JsonError(error_string, status=401)


def JsonResponseForbidden(error_string):
    return JsonError(error_string, status=403)


def JsonResponseNotFound(error_string):
    return JsonError(error_string, status=404)


def JsonResponseNotAllowed(error_string):
    return JsonError(error_string, status=405)


def JsonResponseNotAcceptable(error_string):
    return JsonError(error_string, status=406)


# For backwards compatability purposes
JSONResponse = JsonResponse
JSONError = JsonError
