from flask_restx import Api

from .lists import api as list_namespace
from .items import api as item_namespace
# etc etc.

api = Api(
    title='v1 api',
)

api.add_namespace(list_namespace)
api.add_namespace(item_namespace)