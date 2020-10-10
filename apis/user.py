from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import UserModel

import logging

api = Namespace('user', description='list operations')


@api.route('/')
class Users(Resource):

    def get(self):
        if request.args.get('email'):
            UserModel.query(UserModel.email = request.args.get('email'))

    def post(self):
        user_id = UserModel.count() + 1
        params = request.args
        new_usr = UserModel(
            user_id=user_id,
            email=params['email'],
            password=params['password']
        ).save()
        # serialize new_usr
        return new_usr


@api.route('/<user_id>')
class SingleList(Resource):

    def delete(self, user_id):
        params = request.args
        UserModel.delete(user_id)
        return {'deleted': 'true'}
    
    def get(self, list_id):
        lm = ListModel.query(list_id)
        # serialize lm
        return lm
    