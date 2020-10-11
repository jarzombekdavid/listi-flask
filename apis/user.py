from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import UserModel

import logging

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
    
    def get(self, user_id):
        usr = UserModel.get(user_id)
        return usr.to_dict(), 200
    