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
        # All attributes are projected
        projection = AllProjection()
    email = UnicodeAttribute(hash_key=True)

class Comment(MapAttribute):
    comment_id = NumberAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    comment = UnicodeAttribute()


class Item(MapAttribute):
    item_id = NumberAttribute(hash_key=True)
    source_person = UnicodeAttribute()
    free_text = UnicodeAttribute()
    item_dicts = JSONAttribute()

# create new basemodel to add to_dict for easy serialization
class BaseModel(Model):
    def to_dict(self):
        rval = {}
        for key in self.attribute_values:
            rval[key] = self.__getattribute__(key)
        return rval


class ListModel(BaseModel):
    class Meta:
        table_name = 'lists'
    list_id = NumberAttribute(hash_key=True)
    name = UnicodeAttribute()
    source_person = UnicodeAttribute()
    items = ListAttribute(of=Item)
    comments = ListAttribute(of=Comment)


class UserModel(BaseModel):
    class Meta:
        table_name = 'users'
    user_id = NumberAttribute(hash_key=True)
    email = UnicodeAttribute()
    email_index = EmailIndex()
    password = UnicodeAttribute()
    lists = ListAttribute(default=[])


if not ListModel.exists():
    ListModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
