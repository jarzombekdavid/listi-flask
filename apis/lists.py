from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import ListModel, UserModel

import logging

api = Namespace('lists', description='list operations')


@api.route('/')
class Lists(Resource):

    def get(self):
        params = request.args
        # get listids a user has access to
        user_lists = UserModel.query(params.get('user_id', 0))
        list_ids = [i.user_id for i in user_lists]
        # get list names/ids
        list_data = ListModel.batch_get(list_ids)
        list_names = [(n.name, n.list_id) for n in list_data]
        return list_names

    def post(self):
        params = request.args
        # the below 2 actions should be made into a transaction
        # I am to lazy to at the moment
        lm = ListModel(
            hash_key=str(uuid4()),
            list_name=params['list_name'],
            # items (make util func to handle what the front end gives us)
        ).save()
        usr = UserModel.user_id(params['user_id'])
        usr.lists.append(lm.list_id)
        return {'created': 'true'}


@api.route('/<list_id>')
class SingleList(Resource):

    def delete(self, list_id):
        params = request.args
        ListModel.delete(list_id)
        return {'deleted': 'true'}
    
    def get(self, list_id):
        lm = ListModel.query(list_id)
        # serialize lm
        return lm
    