from uuid import uuid4
from flask import request, session
from .models import UserModel, ListModel


def get_lists():
    usr = UserModel.safe_get(session['current_user'])
    if not usr:
        flask.abort(404, message='user not found')
    if usr.lists:
        list_data = [(n.name, n.list_id) for n in ListModel.batch_get(usr.lists)]
        return list_data
    else:
        return []


def get_single_list(list_id):
    lm = ListModel.safe_get(list_id)
    if lm:
        return lm.to_dict()
    except:
        flask.abort(404, message='list not able to be retrieved')
    

def delete_list(list_id):
    ListModel.delete(list_id)


def create_list(name):
    new_id = str(uuid4())
    lm = ListModel(
        hash_key=new_id,
        name=name,
        source_user=session['current_user'])
    lm.save()
    usr = UserModel.safe_get(session['current_user'])
    usr.lists.append(new_id)
    usr.save()


def get_items(list_id):
    lm = ListModel.safe_get(str(list_id))
    if not lm:
        flask.abort(400, message='failed to retrieve list')
    if not lm.items:
        return []
    else:
        item_ids = lm.items.as_dict().keys()
        items = [lm.items[i] for i in list(item_ids) if lm.items[i]]
        return items


def create_item(list_id, item_id):
    lm = ListModel.safe_get(list_id)
    new_item_id = str(uuid4())
    lm.items[new_item_id] = {
        'item_id': new_item_id,
        'source_user': session['current_user'],
        'free_text': request.args['free_text'],
        'item_dict': request.args.get('item_dict', {})
    }
    lm.save()

def update_item(list_id, item_id):
    lm = ListModel.safe_get(list_id)
    if not lm:
        flask.abort(404, message='no list found')
    lm.update(
        actions=[
            ListModel.items[item_id].set(
                'item_id': item_id,
                'source_user': lm.items[item_id]['source_user'],
                'free_text': request.args.['free_text'],
                'item_dict': request.args.['item_dict']
            )
        ]
    )


def delete_item(list_id, item_id):
    lm = ListModel.get(list_id)
    lm.items[item_id] = {}
    lm.save()