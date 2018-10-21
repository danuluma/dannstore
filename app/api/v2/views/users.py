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


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, help='please enter a username', location='json')
parser.add_argument('password', type=str, help='password can\'t be empty', location='json')
parser.add_argument('action', type=str, help='either promote or demote', location='json')
parser.add_argument('user_id', type=int, help='user id', location='json')
parser.add_argument('access_token', location='json')


def find_user(param, which_row):
  """Finds and returns a user by supplied param."""

  args = parser.parse_args()
  user = UserModel().get_single_user(param, which_row)
  return user


def validate_password(passw):
  """Validates password."""

  return True if re.match("^(?=.*[A-Za-z])(?=.*[\d!@#$%&*?.])[A-Za-z\d!@#$%&*?.]{6,12}$", passw) else False


def validate_username(username):
  """Validates username"""

  return True if re.match("^[A-Za-z\d]{4,10}$", username) else False


def get_role(action):
  """Maps role from input to a digit (0 or 1)"""

  if action == "demote":
    return 1
  if action == "promote":
    return 0


class Register(Resource):
  """Maps to /reg endpoint"""

  @jwt_required
  def post(self):
    """Endpoint to register a new user"""

    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()

    user = find_user(username, 1)
    if user:
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
    if role == 0:
      try:
        UserModel.add_new_user(self, new_user)
      except:
        return {"Error":"Username already exists"}, 409
      return {'Message': "Success! User created"}, 201
    return {'Error': 'Only admins are allowed to add users'}, 401


class Login(Resource):
  """Maps to /reg endpoint"""

  def post(self):
    """Endpoint to login a user and create an access token"""

    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()

    user = find_user(username, 1)
    if not user:
      return {'Error': 'Wrong password or username'}, 400

    if password != user['password']:
      return {'Error': 'Wrong password or username'}, 400

    user_details = [user['id'], user['username'], user['role']]
    access_token = create_access_token(identity=user_details)

    mesg = {
        'access_token': access_token,
    }
    return mesg, 200


class User(Resource):
  """Maps to /users/userID endpoint."""

  @jwt_required
  def get(self, userID):
    """Retrieves a user by userID."""

    current_user = get_jwt_identity()
    role = current_user[2]
    if role == 0:
      user = UserModel().get_single_user(userID, 0)
      return user, 200
    return {"Error": "Only admins can view other users"}, 401

  @jwt_required
  def put(self, userID):
    """Endpoint to promote/demote a user."""

    args = parser.parse_args()
    action = args['action']
    role = get_role(action)

    current_user = get_jwt_identity()
    my_id = current_user[0]
    if my_id == 1:
      user = UserModel.get_single_user(self, userID, 0)
      if not user:
        return {'Error': 'User by that id does not exist'}, 404
      try:
        UserModel().promote_demote_user(userID, role)
      except:
        return {"Error":"Error"}, 404
      return {'Message': "Success! User promoted to an admin"}, 201
    return {"Error": "Only the owner can promote or demote"}, 401


class Users(Resource):
  """Maps to /users endpoint"""

  @jwt_required
  def get(self):
    """ Returns all users in the database"""

    current_user = get_jwt_identity()
    role = current_user[2]
    if role == 0:
      return UserModel().get_all_users(), 200
    return {"Error": "Only admins can view all users"}, 401

  @jwt_required
  def delete(self):
    """Deletes a user. Requires the user Id"""


    args = parser.parse_args()
    user_id = args['user_id']
    current_user = get_jwt_identity()
    uid = current_user[0]
    if uid == 1:
      try:
        UserModel().delete_user(user_id)
      except:
        return {"Error":"Error"}, 404
      return {'Message': "Success! That user has been deleted"}, 201
    return {"Error": "Only the owner can delete attendats"}, 401