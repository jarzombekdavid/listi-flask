from flask import request, g, session
from flask_restx import abort
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from pynamodb.models import DoesNotExist

from .database import UserModel

import logging


def authenticate():
    if not (request.method in ['GET', 'POST'] and str(request.url_rule) in ['/', '/user/login']):
        token = verify_token(request.headers.get('Token'))
        if not token:
            abort(401)
        return token['user_id']


def authenticate_list_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        list_id = request.args.get('list_id')
        if kwargs and not list_id:
            list_id = kwargs.get('list_id')
        try:
            user = UserModel.get(g.user_id)
        except DoesNotExist:
            abort(400, 'no user found')
        if list_id and user and list_id in user.lists:
            return func(*args, **kwargs) 
        if list_id:
            abort(404, 'not authorized, list authentication failure for user')
        return func(*args, **kwargs)
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
    if not token:
        abort(400, 'token required')
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return {}
    return data
    
def verify_password(email, password):
    user = UserModel.email_index.query(email)
    user = [u for u in user]
    if not user:
        abort(400, 'user not found')
    elif password != user[0].password:
        abort(400, 'incorrect password')
    return {'token': generate_token(user[0]), 'user_id': user[0].user_id}, 200
