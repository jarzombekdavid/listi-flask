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
            usr = UserModel.email_index.query(request.args.get('email'))
            usr = [u for u in usr]
            # import pdb; pdb.set_trace()
            if usr:
                return usr[0].to_dict()
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

        usr = UserModel.get(int(user_id))
        usr.delete()
        return {"status": 'deleted'}

    def get(self, user_id):
        # change user id to int because it comes as str by default
        # this is one nice thing about fastapi...
        usr = UserModel.get(int(user_id))
        return usr.to_dict()
