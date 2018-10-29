from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
import re


users = [
]


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True,
                    help='please enter a username', location='json')
parser.add_argument('password', type=str, required=True,
                    help='password can\'t be empty', location='json')
parser.add_argument(
    'role', type=int, help='enter user access level', location='json')
parser.add_argument('access_token', location='json')


def find_user(username):
    """Finds and returns a user by username."""

    args = parser.parse_args()
    user = [user for user in users if user['username'] == username]
    return user


def create_admin():
    """Creates the default admin account."""

    users.append({
        "id": 0,
        "username": "owner",
        "password": "secret1",
        "role": 0
    })


def clear_users():
    """Clears the users list"""

    users.clear()


def validate_password(passw):
    """Validates password."""

    return True if re.match("^(?=.*[A-Za-z])(?=.*[\d!@#$%&*?.])[A-Za-z\d!@#$%&*?.]{6,12}$", passw) else False


def validate_username(username):
    """Validates username"""

    return True if re.match("^[A-Za-z\d]{4,10}$", username) else False


class Register(Resource):
    """Maps to /reg endpoint"""

    @jwt_required
    def post(self):
        """Endpoint to register a new user"""

        args = parser.parse_args()
        username = args['username'].strip()
        password = args['password'].strip()
        role = args['role']

        user = find_user(username)
        error = []
        if len(user) != 0:
            return {'Error': 'Username already exists'}, 409
        if validate_username(username) != True:
            error.append({'Error': 'Please input a valid username'})
        if validate_password(password) != True:
            error.append({'Error': 'Please input a valid password'})
        if len(error) > 0:
            return error, 400
        new_user = {
            'id': len(users) + 1,
            'username': username,
            'password': password,
            'role': role
        }
        current_user = get_jwt_identity()
        if current_user[2] == 0:
            users.append(new_user)
            return {'message': "Success!"}, 200
        return {'Error': 'Only admins are allowed to add users'}, 401


class Login(Resource):
    """Maps to /reg endpoint"""

    def post(self):
        """Endpoint to login a user and create an access token"""

        args = parser.parse_args()
        username = args['username'].strip()
        password = args['password'].strip()

        user = find_user(username)
        if len(user) == 0:
            return {'Error': 'Username does not exist'}, 404

        if password != user[0]['password']:
            return {'Error': 'Wrong password'}, 401

        user_details = [user[0]['id'], user[0]['username'], user[0]['role']]
        access_token = create_access_token(identity=user_details)

        mesg = {
            'access_token': access_token,
        }
        return mesg, 201
