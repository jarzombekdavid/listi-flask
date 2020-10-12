from flask import request, g
from flask_restx import abort
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from .database import UserModel


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.args.get('token'):
            abort(401, message='requires authorization token')
        token = verify_token(request.args.get('token'))
        if token:
            g.current_user = token['user_id']
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
    
def verify_password(email, password):
    user = UserModel.email_index.query(email)
    user = [u for u in user]
    if not user:
        abort(400, message='user not found')
    elif password != user[0].password:
        abort(400, message='incorrect password')
    return {'token': generate_token(user[0]), 'user_id': user[0].user_id}, 200
    