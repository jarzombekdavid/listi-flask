import json

from uuid import uuid4
from flask import request, g
from flask_restx import Namespace, Resource
from .database import ListModel, UserModel
from .auth import authenticate, authenticate_list_access

import logging

api = Namespace(
    'lists',
    description='list operations',
    decorators=[authenticate, authenticate_list_access]
)


@api.route('')
class Lists(Resource):
    def get(self):
        usr = UserModel.get(session['current_user'])
        list_data = [(n.name, n.list_id) for n in ListModel.batch_get(usr.lists)]
        return list_data

    @api.doc(params={'name': 'list name'})
    def post(self):
        params = request.args
        body = request.json
        new_id = str(uuid4())
        lm = ListModel(
            hash_key=new_id,
            name=body['name'],
            source_user=params['user_id']
        )
        lm.save()
        usr = UserModel.get(session['current_user'])
        usr.lists.append(new_id)
        usr.save()
        return {'action': f'new list created: {body["name"]}'}, 201


@api.route('/<list_id>')
class SingleList(Resource):
    def delete(self, list_id):
        ListModel.delete(list_id)
        return {'action': 'delete successful'}, 200

    def get(self, list_id):
        lm = ListModel.get(list_id)
        return lm.to_dict(), 200

@api.route('/<list_id>/items')
class ListItems(Resource):
    def get(self, list_id):
        lm = ListModel.get(str(list_id))
        item_ids = lm.items.as_dict().keys()
        items = [lm.items[i] for i in list(item_ids) if lm.items[i]]
        return items, 200

    @api.doc(params={'free_text': 'free text for item', 'item_dict': 'json of attributes for item'})
    def post(self, list_id): #may need to be put
        lm = ListModel.get(list_id)
        new_item_id = str(uuid4())
        lm.items[new_item_id] = {
            'item_id': new_item_id,
            'source_user': session['current_user'],
            'free_text': request.args['free_text'],
            'item_dict': request.args.get('item_dict', {})
        }
        lm.save()
        return {'action': 'added item to list'}, 200


@api.route('/<list_id>/items/<item_id>')
class ListItem(Resource):
    @api.doc(params={
        'free_text': 'free text for item (optional)',
        'item_dict': 'json of attributes for item (optional)'})
    def put(self, list_id, item_id):
        lm = ListModel.get(list_id)
        lm.items[item_id] = {
            'item_id': item_id,
            'source_user': lm.items[item_id]['source_user'],
            'free_text': request.args.get('free_text', lm.items[item_id]['free_text']),
            'item_dict': request.args.get('item_dict', lm.items[item_id]['item_dict']),
        }
        lm.save()
        return {'action': 'updated list item'}, 200

    def delete(self, list_id, item_id):
        lm = ListModel.get(list_id)
        lm.items[item_id] = {}
        lm.save()
        return {'action': 'item of list deleted'}, 200
