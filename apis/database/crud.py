from uuid import uuid4
import json
from flask import request, session, g
from .models import UserModel, ListModel, ItemModel
from pynamodb.models import DoesNotExist


def get_lists():
    try:
        usr = UserModel.get(g.user_id)
    except DoesNotExist:
        flask.abort(404, 'user not found')
    return [(n.name, n.list_id) for n in ListModel.batch_get(usr.lists)]


def get_single_list(list_id):
    try:
        lm = ListModel.get(list_id)
    except DoesNotExist:
        flask.abort(404, 'no list with given id')
    return lm.to_dict()


def delete_list(list_id):
    try:
        ListModel.delete(list_id)
    except DoesNotExist:
        flask.abort(404, 'no list with given id')


def create_list(params):
    new_id = str(uuid4())
    lm = ListModel(
        hash_key=new_id,
        name=params['name'],
        source_user=g.user_id)
    lm.save()
    usr = UserModel.get(g.user_id)
    usr.lists.append(new_id)
    usr.save()
    return new_id


def get_items(list_id):
    try:
        lm = ListModel.get(list_id)
    except DoesNotExist:
        flask.abort(400, 'failed to retrieve list')
    item_ids = lm.items.as_dict().keys()
    return [lm.items[i] for i in list(item_ids) if lm.items[i]]


def create_item(list_id):
    lm = ListModel.get(list_id)
    new_item_id = str(uuid4())
    data = json.loads(request.data)
    lm.items[new_item_id] = {
        'item_id': new_item_id,
        'source_user': g.user_id,
        'free_text': request.args.get('free_text', ''),
        'item_dict': data
    }
    lm.save()
    # update the list item model
    item_keys = list(data.keys())
    try:
        im = ItemModel.get(list_id)
        im.keys = item_keys
    except:
        im = ItemModel(
            list_id=list_id,
            keys=item_keys
        )
    finally:
        im.save()

def get_item_keys(list_id):
    im = ItemModel.get(list_id)
    return im.keys

def update_item(list_id, item_id, params):
    try:
        lm = ListModel.get(list_id)
    except DoesNotExist:
        flask.abort(404, 'no list found')
    lm.update(
        actions=[
            ListModel.items[item_id].set(
                {
                    'item_id': item_id,
                    'source_user': lm.items[item_id]['source_user'],
                    'free_text': params['free_text'],
                    'item_dict': params['item_dict']
                }
            )
        ]
    )


def delete_item(list_id, item_id):
    try:
       lm = ListModel.get(list_id)
    except DoesNotExist:
        flask.abort(404, 'list not found, cannot delete item')
    lm.items[item_id] = {}
    lm.save()
