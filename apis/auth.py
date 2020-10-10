from uuid import uuid4
from flask import request, g, jsonify
from flask_restx import Namespace, Resource
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from .database import UserModel
import logging

api = Namespace('', description='login/authorization operations')

def generate_token(user, expiration=TWO_WEEKS):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'id': user.id,
        'email': user.email,
    }).decode('utf-8')
    return token

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data




@api.route('/login')
class Login(Resource):
    def get(self):
        email, password = request.args.get('email'), request.args.get('password')
        if request.args.get('email'):
            usr = UserModel.email_index.query(request.args.get('email'))
            usr = [u for u in usr]

            if usr:
                return usr[0].as_dict()
            else:
                return {}
        else:
            return 'require email'

    def post(self):
        user_id = UserModel.count() + 2
        params = request.args
        new_usr = UserModel(
            user_id,
            email=params['email'],
            password=params['password']
        ).save()
        return {'new_user': user_id}


@api.route('/<user_id>')
class SingleUser(Resource):
    def delete(self, user_id):
        params = request.args
        usr = UserModel.get(user_id)
        usr.delete()
        return {'deleted'}
    
    def get(self, user_id):
        usr = UserModel.get(user_id)
        return usr.to_dict()
    