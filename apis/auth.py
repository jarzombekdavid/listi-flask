from uuid import uuid4
from flask import request, g, jsonify
from flask_restx import Namespace, Resource
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from .database import UserModel
import logging

api = Namespace('', description='login/authorization operations')


def authenticate(func):
    # assumes a returned token in requests call
    @wraps(func)
    def wrapper(*args, **kwargs):
        token, user_id = request.args.get('Authentication'), kwargs.get('user_id')
        token = verify_token()
        if token.get('user_id') == user_id:  # verify user is the user in the api call
            return func(*args, **kwargs)
        if requests.args.get('list_id') and token.get('user_id'):
            user = UserModel.get('user_id')
            if requests.args.get('list_id') in user.lists:  # if trying to access list, verify autheticated user has that access
                return func(*args, **kwargs)
        flask_restx.abort(401)
    return wrapper

def generate_token(user, expiration=TWO_WEEKS):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'user_id': user.user_id,
        'email': user.email,
    }).decode('utf-8')
    return token

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return {}
    return data


@api.route('/login')
class Login(Resource):
    def get(self):
        email, password = request.args.get('email'), request.args.get('password')
        if request.args.get('email'):
            usr = UserModel.email_index.query(request.args.get('email'))
            usr = [u for u in usr]
            if usr:
                return generate_token(user)
            else:
                return {}
        else:
            return {'error': 'require email'}
    