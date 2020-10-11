from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, JSONAttribute, NumberAttribute


# hash key is an index
# range key is an aditional search param
# can really only search based on those 2 things

# need an index on the email user so its easy to search by email for login purposes
class EmailIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected -- I'm not sure what this does
        projection = AllProjection()
    email = UnicodeAttribute(hash_key=True)

# Comment and Item are nested inside the lists and have their own classes
class CommentAttr(MapAttribute):
    comment_id = UnicodeAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    comment = UnicodeAttribute()


class ItemAttr(MapAttribute):
    item_id = UnicodeAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    free_text = UnicodeAttribute()
    item_dicts = JSONAttribute()
    comments = MapAttribute(of=CommentAttr, default={})


# create new basemodel to add to_dict for easy serialization
class BaseModel(Model):
    def to_dict(self):
        rval = {}
        for key in self.attribute_values:
            rval[key] = self.__getattribute__(key)
            if isinstance(rval[key], MapAttribute):
                rval[key] = rval[key].as_dict()
        return rval


class ListModel(BaseModel):
    class Meta:
        table_name = 'lists'
    list_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    source_user = UnicodeAttribute()
    items = MapAttribute(of=ItemAttr, default={})
    


class UserModel(BaseModel):
    class Meta:
        table_name = 'users'
    user_id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    email_index = EmailIndex()
    password = UnicodeAttribute()
    lists = ListAttribute(default=[])


if not ListModel.exists():
    ListModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
