from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, JSONAttribute, NumberAttribute


# hash key is an index
# sort key is an aditional search param
# can really only search based on those 2 things

class Comment(MapAttribute):
    comment_id = NumberAttribute(sort_key=True)
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
    username = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute(sort_key=True)
    password = UnicodeAttribute()
    lists = ListAttribute()



if not ListModel.exists():
    ListModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
