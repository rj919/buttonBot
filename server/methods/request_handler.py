__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

from jsonmodel.validators import jsonModel

def requestDeconstructor(request_object, request_schema):

    request_details = {}
    request_model = jsonModel(request_schema)

    try:
        request_details = request_object.get_json(silent=True)
    except:
        return request_details

    if not request_details:
        return request_details

    request_details = request_model.ingest(**request_details)

    return request_details
