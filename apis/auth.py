from flask import request
from flask_restx import abort
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from .database import UserModel


def authenticate(func):
    # assumes a returned token in request call
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            abort(401, message='requires authorization token')
        token = verify_token(token)
        if token.get('user_id') == request.args['user_id']:  # verify user is the user in the api call
            return func(*args, **kwargs)
        if request.args.get('list_id') and token.get('user_id'):
            user = UserModel.get(token.get('user_id'))
            raise ValueError(user.to_dict())
            if request.args.get('list_id') in user.lists:  # if trying to access list, verify autheticated user has that access
                return func(*args, **kwargs)
        abort(401)
    return wrapper

def generate_token(user, expiration=1000000):
    s = Serializer('SECRETKEY', expires_in=expiration)
    token = s.dumps({
        'user_id': user.user_id,
        'email': user.email,
    }).decode('utf-8')
    return token

def verify_token(token):
    s = Serializer('SECRETKEY')
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return {}
    return data



    