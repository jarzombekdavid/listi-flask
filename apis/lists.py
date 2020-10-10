from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import ListModel, UserModel, ItemAttr

import logging

api = Namespace('lists', description='list operations')


@api.route('/')
class Lists(Resource):
    def get(self):
        params = request.args
        usr = UserModel.get(int(params['user_id']))
        list_data = [(n.name, n.list_id) for n in ListModel.batch_get(usr.lists)]
        return list_names
    def post(self):
        params = request.args
        lm = ListModel(
            hash_key=str(uuid4()),
            list_name=params['list_name'],
            source_user=params['user_id']
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
        lm = ListModel.get(list_id)
        return lm.to_dict()
    
@api.route('/<list_id>/items')
class ListItems(resource):
    def get(self, list_id):
        lm = ListModel.get(str(list_id))
        item_ids = lm.items.as_dict().keys()
        items = [lm.items[i] for i in list(item_ids) if lm.items[i]]
        return items

    def post(self, list_id): #may need to be put
        params = request.args
        lm = ListModel.get(str(list_id))
        new_id = str(uuid4())
        lm.items[new_id] = {
            'item_id': str(uuid4())
            'source_user': params['user_id'],
            'free_text': params['free_text'],
            'item_dict': params['item_dict']
        }
        lm.save()

@api.route('/<list_id>/item/<item_id>')
class ListItem(resource):
    def post(self, list_id, item_id)  #may need to be put
        lm = ListModel.get(str(list_id))
        lm.items[item_id] = {
            'item_id': item_id,
            'source_user': params['user_id'],
            'free_text': params['free_text'],
            'item_dict': params['item_dict']
        }
        lm.save()
    
    def delete(self, list_id, item_id):
        lm = ListModel.get(str(list_id))
        lm.items[item_id] = {}
        lm.save()