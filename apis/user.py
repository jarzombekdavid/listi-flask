from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import UserModel

import logging

api = Namespace('user', description='list operations')


@api.route('')
class Users(Resource):

    def get(self):
        if request.args.get('email'):
            UserModel.email_index(request.args.get('email'))
        else:
            return {'require email'}


    def post(self):
        user_id = UserModel.count() + 2
        params = request.args
        new_usr = UserModel(
            user_id,
            email=params['email'],
            password=params['password']
        ).save()
        # serialize new_usr
        return user_id


@api.route('/<user_id>')
class SingleUser(Resource):

    def delete(self, user_id):
        params = request.args
        usr = UserModel.get(str(user_id))
        usr.delete()
        return {}
    
    def get(self, user_id):
        usr = UserModel.get(str(user_id))
        return usr.to_dict()
    