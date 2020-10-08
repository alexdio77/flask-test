import base64
import json
import os
from functools import wraps
from collections import OrderedDict

from flask import request, jsonify, _request_ctx_stack
from werkzeug.local import LocalProxy

from app import app

current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))

JWT_DEFAULT_REALM = os.getenv('JWT_DEFAULT_REALM')


class Identity(object):
    def __init__(self, payload):
        self.sub = payload['sub']
        self.payload = payload


class JWTError(Exception):
    def __init__(self, error, description='', status_code=401, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'JWTError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)


def _jwt_error_handler(error):
    return jsonify(OrderedDict([
        ('status_code', error.status_code),
        ('error', error.error),
        ('description', error.description),
    ])), error.status_code, error.headers

def _jwt_payload(bearer: str):
    jwt_value = bearer.split(' ')[-1]
    try:
        headers_enc, payload_enc, verify_signature = jwt_value.split(".")
    except ValueError:
        raise JWTError('Invalid token')

    payload_enc += '=' * (-len(payload_enc) % 4)  # add padding
    try:
        payload = json.loads(base64.b64decode(payload_enc).decode("utf-8"))
    except json.decoder.JSONDecodeError:
        raise JWTError('Invalid token payload')
    return payload

def _jwt_payload_validate(payload, realm=None):
    # azp - Authorized party - the party to which the ID Token was issued
    if realm and payload.get('azp') != realm:
        raise JWTError(
            'Authorization Required', 
            f'Not authorized for realm {realm}',
            headers={'WWW-Authenticate': f'JWT realm="{realm}"'}
        )
    if payload.get("sub") is None:
        raise JWTError('Invalid JWT', 'User does not exist')

    return payload


def jwt_required(realm=None):
    """View decorator that requires a valid JWT token to be present in the request
    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            bearer = request.headers.get('Authorization')
            if not bearer:
                raise JWTError(
                    'Authorization Required', 
                    'Request does not contain an access token',
                    headers={'WWW-Authenticate': f'JWT realm="{realm}"'}
                )
            payload = _jwt_payload(bearer)
            payload = _jwt_payload_validate(payload, realm or JWT_DEFAULT_REALM)
            _request_ctx_stack.top.current_identity = Identity(payload)
            return fn(*args, **kwargs)
        return decorator
    return wrapper


app.errorhandler(JWTError)(_jwt_error_handler)
