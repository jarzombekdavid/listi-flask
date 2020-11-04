import json

from uuid import uuid4
from flask import request, g
from flask_restx import Namespace, Resource
from .database import ListModel, UserModel, crud
from .auth import authenticate_list_access

import logging

api = Namespace(
    'lists',
    description='list operations',
    decorators=[authenticate_list_access]
)


@api.route('')
class Lists(Resource):
    def get(self):
        list_data = crud.get_lists()
        return list_data, 200

    @api.doc(params={'name': 'list name'})
    def post(self):
        # TODO: decide if name should be in params or body
        params = {
            "name": request.args.get("name",
                request.json.get("name")
            )
        }
        id = crud.create_list(params)
        return {'action': 'new list created', 'id': id}, 201


@api.route('/<list_id>')
class SingleList(Resource):
    def delete(self, list_id):
        crud.delete_list(list_id)
        return {'action': 'delete successful'}, 200

    def get(self, list_id):
        lm = crud.get_single_list(list_id)
        return lm, 200


@api.route('/<list_id>/items')
class ListItems(Resource):
    def get(self, list_id):
        items = crud.get_items(list_id)
        return items, 200

    @api.doc(params={
        'free_text': 'free text for item',
        'item_dict': 'json of attributes for item'})
    def post(self, list_id):
        crud.create_item(list_id)
        return {'action': 'added item to list'}, 200


@api.route('/<list_id>/items/<item_id>')
class ListItem(Resource):
    @api.doc(params={
        'free_text': 'free text for item (optional)',
        'item_dict': 'json of attributes for item (optional)'})
    def put(self, list_id, item_id):
        crud.update_item(list_id, item_id, request.args)
        return {'action': 'updated list item'}, 200

    def delete(self, list_id, item_id):
        crud.delete_item(list_id, item_id)
        return {'action': 'item of list deleted'}, 200

@api.route('/<list_id>/items/keys')
class ListItemKey(Resource):
    @api.doc()
    def get(self, list_id):
        return crud.get_item_keys(list_id)
