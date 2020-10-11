from flask_restx import Api

from .lists import api as list_namespace
from .user import api as user_namespace
from .auth import api as auth_namespace
# etc etc.

api = Api(
    title='listi v1 api',
)

api.add_namespace(list_namespace)
api.add_namespace(user_namespace)
api.add_namespace(auth_namespace)