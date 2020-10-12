from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource
from .database import UserModel
from .auth import generate_token, authenticate


api = Namespace(
    'user',
    description='list operations'
)

parser = api.parser()
parser.add_argument('email', type=str,)
parser.add_argument('password', type=str)


@api.route('')
class Users(Resource):
    @api.expect(parser)
    def post(self):
        user_id = str(uuid4())
        params = request.args
        new_usr = UserModel(
            user_id,
            email=params['email'],
            password=params['password']
        ).save()
        return {'new_user': user_id}, 201


@api.route('/<user_id>')
class SingleUser(Resource):
    def delete(self, user_id):
        method_decorators=[authenticate]
        params = request.args
        usr = UserModel.get(user_id)
        usr.delete()
        return {'action': 'user deleted'}, 200


@api.route('/login')
class Login(Resource):
    @api.expect(parser)
    @api.doc(params={'email': 'email', 'password': 'password'})
    def post(self):
        return verify_password(request.args['email'], request.args['password'])

    
