from django.http import HttpResponse

try:
    import simplejson as json
except ImportError:
    import json

# JSON helper functions

def JSONResponse(data, dump=True):
    try:
        data['errors']
    except KeyError:
        data['success'] = True
    except TypeError:
        pass

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
