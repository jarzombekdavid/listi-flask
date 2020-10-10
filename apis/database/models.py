from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, JSONAttribute, NumberAttribute


class Comment(MapAttribute):
    comment_id = NumberAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    comment = UnicodeAttribute()


class Item(MapAttribute):
    item_id = NumberAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    free_text = UnicodeAttribute()
    item_dicts = JSONAttribute()


class ListModel(Model):
    class Meta:
        table_name = 'lists'
    list_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()
    source_person = UnicodeAttribute()
    items = ListAttribute(of=Item)
    comments = ListAttribute(of=Comment)


class UserModel(Model):
    class Meta:
        table_name = 'users'
    user_id = NumberAttribute(hash_key=True)
    email = UnicodeAttribute()
    password = UnicodeAttribute()
    lists = ListAttribute(of=NumberAttribute)



if not ListModel.exists():
    ListModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
