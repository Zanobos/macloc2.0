from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def bad_request(message):
    return error_response(400, message=message)

def unauthorized(message):
    return error_response(401, message=message)

def error_response(status_code, error_type='TECHNICAL', message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unkown error'), 'errorType':error_type}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
