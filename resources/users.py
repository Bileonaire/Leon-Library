"""Contains all endpoints to manipulate user information
"""
import datetime

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, inputs
import jwt

import models
import config
from .auth import admin_required, token_required

class Signup(Resource):
    "Contains a POST method to register a new user"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get('email'):
                return jsonify({"message" : "user with that email already exists"})

        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.create_user(**kwargs)
                return make_response(jsonify(result), 201)
            return make_response(jsonify({"message" : "password should be atleast 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and cofirm password should be identical"}), 400)

class Login(Resource):
    "Contains a POST method to login a user"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """login a user"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get("email") and \
                models.all_users.get(user_id)["password"] == kwargs.get("password"):
                
                token = jwt.encode({
                'id' : user_id,
                'admin' : models.all_users.get(user_id)["admin"],
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(weeks=2)},
                               config.Config.SECRET_KEY)

                return make_response(jsonify({
                "message" : "success, add the token to the header as x-access-token for authentication",
                "token" : token.decode('UTF-8')}), 200)
                return make_response(jsonify({"message" : "you have been successfully logged in"}), 200)
        return make_response(jsonify({"message" : "invalid email address or password"}), 400)



class UserList(Resource):
    "Contains a POST method to register a new user and a GET method to get all users"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get('email'):
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.create_user(**kwargs)
                return make_response(jsonify(result), 201)
            return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
    
    @admin_required
    def get(self):
        """Get all users"""
        return make_response(jsonify(models.all_users), 200)


class User(Resource):
    """Contains GET PUT and DELETE methods for interacting with a particular user"""


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def get(self, user_id):
        """Get a particular user"""
        try:
            user = models.all_users[user_id]
            return make_response(jsonify(user), 200)
        except KeyError:
            return make_response(jsonify({"message" : "user does not exist"}), 404)
    
    @admin_required
    def put(self, user_id):
        """Update a particular user"""
        kwargs = self.reqparse.parse_args()
        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.update_user(user_id, **kwargs)
                if result != {"message" : "user does not exist"}:
                    return make_response(jsonify(result), 200)
                return make_response(jsonify(result), 404)
            return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
    
    @admin_required
    def delete(self, user_id):
        """Delete a particular user"""
        result = models.User.delete_user(user_id)
        if result != {"message" : "user does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

# class ResetPassword(Resource):
#     "Contains a POST method to reset password"


#     def __init__(self):
#         "Validates input from the form as well as json input"
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument(
#             'password',
#             required=True,
#             trim=True,
#             help='kindly provide a valid password',
#             location=['form', 'json'])
#         self.reqparse.add_argument(
#             'new password',
#             required=True,
#             trim=True,
#             help='kindly provide a valid password',
#             location=['form', 'json'])
#         self.reqparse.add_argument(
#             'confirm new password',
#             required=True,
#             trim=True,
#             help='kindly provide a valid password',
#             location=['form', 'json'])
#         super().__init__()

#     @token_required
#     def post(self):
#         """reset user password"""
#         kwargs = self.reqparse.parse_args()
#         data = jwt.decode(token, config.Config.SECRET_KEY)
#         admin = data['admin']
#         user_id = data['id']
#         if models.all_users.get(user_id)["password"] == kwargs.get('current password'):
#             if kwargs.get("new password") == kwargs.get('confirm new password'):
#                 if len(kwargs.get('password')) >= 8:
#                     password = kwargs.get('new password')
#                     username = models.all_users.get(user_id)["username"]
#                     email = models.all_users.get(user_id)["username"]
#                     models.User.update_user(user_id, username, email, password, admin)
                
#                     return make_response(jsonify({"message" : "you have successfully changed your password"}), 200)
#                 return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
#             return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
#         return make_response(jsonify({"message" : "invalid password"}), 400)


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(Signup, '/auth/register', endpoint='register')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
api.add_resource(User, '/users/resetpassword', endpoint='resetpassword')
