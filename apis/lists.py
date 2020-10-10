import json

from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import ListModel, UserModel

import logging

api = Namespace('lists', description='list operations')


@api.route('')
class Lists(Resource):
    @api.doc(params={'user_id': 'active_user'})
    def get(self):
        params = request.args
        usr = UserModel.get(int(params['user_id']))
        list_data = [(n.name, n.list_id) for n in ListModel.batch_get(usr.lists)]
        return list_data
    @api.doc(params={'user_id': 'active_user', 'name': 'list name'})
    def post(self):
        params = request.args
        new_id = str(uuid4())
        lm = ListModel(
            hash_key=new_id,
            name=params['name'],
            source_user=params['user_id']
        ).save()
        usr = UserModel.get(int(params['user_id']))
        usr.lists.append(new_id)
        usr.save()
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
class ListItems(Resource):
    @api.doc('gets all items for a given list')
    def get(self, list_id):
        lm = ListModel.get(str(list_id))
        item_ids = lm.items.as_dict().keys()
        items = [lm.items[i] for i in list(item_ids) if lm.items[i]]
        return items
    
    @api.doc(params={'user_id': 'active_user', 'free_text': 'free text for item', 'item_dict': 'json of attributes for item'})
    def post(self, list_id): #may need to be put
        params = request.args
        lm = ListModel.get(str(list_id))
        new_id = str(uuid4())
        lm.items[new_id] = {
            'item_id': new_id,
            'source_user': params['user_id'],
            'free_text': params['free_text'],
            'item_dict': params.get('item_dict', {})
        }
        lm.save()
        return {'added': 'true'}


@api.route('/<list_id>/items/<item_id>')
class ListItem(Resource):
    @api.doc(params={
        'user_id': 'active_user (optional)',
        'free_text': 'free text for item (optional)',
        'item_dict': 'json of attributes for item (optional)'})
    def post(self, list_id, item_id):  #may need to be put
        params = request.args
        lm = ListModel.get(str(list_id))
        lm.items[item_id] = {
            'item_id': item_id,
            'source_user': params.get('user_id', lm.items[item_id]['source_user']),
            'free_text': params.get('free_text', lm.items[item_id]['free_text']),
            'item_dict': params.get('item_dict', lm.items[item_id]['item_dict']),
        }
        lm.save()
        return {'updated': 'true'}
    
    def delete(self, list_id, item_id):
        lm = ListModel.get(str(list_id))
        lm.items[item_id] = {}
        lm.save()
        return {'deleted': 'true'}