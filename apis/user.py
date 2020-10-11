from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import UserModel
from .auth import generate_token


api = Namespace('user', description='list operations')


@api.route('')
class Users(Resource):
    def post(self):
        user_id = str(uuid4())
        params = request.args
        new_usr = UserModel(
            user_id,
            email=params['email'],
            password=params['password']
        ).save()
        return {'new_user': user_id}, 201


@api.route('/<user_id>')
class SingleUser(Resource):
    def delete(self, user_id):
        params = request.args
        usr = UserModel.get(user_id)
        usr.delete()
        return {'action': 'user deleted'}, 200


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

    
