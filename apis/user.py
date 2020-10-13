from uuid import uuid4
from flask import request, abort
from flask_restx import Namespace, Resource
from .database import UserModel
from .auth import generate_token, verify_password


api = Namespace(
    'user',
    description='list operations'
)

@api.route('')
class Users(Resource):
    def post(self):
        params = request.args
        existing = UserModel.email_index.query(params['email'])
        existing = [e for e in existing]
        if existing:
            abort(400, 'email exists already')
        user_id = str(uuid4())
        new_usr = UserModel(
            user_id,
            email=params['email'],
            password=params['password']
        ).save()
        return {'new_user': user_id}, 201


@api.route('/<user_id>')
class SingleUser(Resource):
    def delete(self, user_id):
        usr = UserModel.get(user_id)
        usr.delete()
        return {'action': 'user deleted'}, 200


@api.route('/login')
class Login(Resource):
    @api.doc(params={'email': 'email', 'password': 'password'})
    def post(self):
        return verify_password(request.args['email'], request.args['password'])
