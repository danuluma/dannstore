from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
import re
import os, sys
import datetime
import jsonify
import psycopg2


# Local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.user import UserModel


users = UserModel().get_all_users()


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
  user = [user for user in users if user[1] == username]
  return user


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
    if len(user) != 0:
      return {'Error': 'Username already exists'}, 409
    if validate_username(username) != True:
      return {'Error': 'Please input a valid username'}, 400
    if validate_password(password) != True:
      return {'Error': 'Please input a valid password'}, 400
    current_user = get_jwt_identity()
    role = current_user[2]
    my_id = current_user[0]
    new_user = [
        username,
        password,
        my_id
    ]
    # return (new_user)
    role = current_user[2]
    if role == 0:
      try:
        UserModel.add_new_user(self, new_user)
      except psycopg2.IntegrityError:
        return {"Error":"Data already exists"}, 409
      return {'message': "Success!"}, 201
    return {'Error': 'Only admins are allowed to add users'}, 401

  def get(self):
    for i in users:
      return i[1], 200
    # return str(users)


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

    if password != user[0][2]:
      return {'Error': 'Wrong password'}, 401

    user_details = [user[0][0], user[0][1], user[0][3]]
    access_token = create_access_token(identity=user_details)

    mesg = {
        'access_token': access_token,
    }
    return mesg, 200
