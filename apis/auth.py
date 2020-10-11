from uuid import uuid4
from flask import request, g, jsonify
from flask_restx import Namespace, Resource, abort
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from .database import UserModel
import logging

api = Namespace('', description='login/authorization operations')


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


@api.route('/login')
class Login(Resource):
    @api.doc(params={'email': 'email', 'password': 'password'})
    def post(self):
        email, password = request.args.get('email'), request.args.get('password')
        if request.args.get('email'):
            try:
                user = UserModel.email_index.query(request.args.get('email'))
            except:
                return {'error', 'error returning user'}, 400
            user = [u for u in user]
            if user:
                if password != user[0].password:
                    return {'error': 'incorrect password'}, 400
                return {'token': generate_token(user[0]), 'user_id': user[0].user_id}, 200
            else:
                return {'error': 'user not found'}, 404
        else:
            return {'error': 'require email'}, 400
    