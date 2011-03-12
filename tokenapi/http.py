# JSON helper functions
from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json

def JSONResponse(data, dump=True):
    return HttpResponse(
        json.dumps(data) if dump else data,
        mimetype='application/json',
    )

def JSONError(error_string):
    data = {
        'success': False,
        'errors': error_string,
    }
    return JSONResponse(data)
