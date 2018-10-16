from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)


users = [
]


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True, help='please enter a username',  location='json')
parser.add_argument('password', type=str, required=True, help='password can\'t be empty', location='json')
parser.add_argument('role', type=int, help='enter user access level', location='json')
parser.add_argument('access_token', location='json')

def find_user(username):
  args = parser.parse_args()
  user = [user for user in users if user['username'] == username]
  return user

def create_admin():
  users.append({
            "id": 0,
            "username": "owner",
            "password": "secret",
            "role": 0
        })

def clear_users():
  users.clear()

class Register(Resource):
  """Endpoint to register a new user"""
  @jwt_required
  def post(self):
    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()
    role = args['role']

    user = find_user(username)
    if len(user) != 0:
      return {'Error':'Username already exists'}, 409
    if username == "":
      return {'Error':'Please input a valid username'}, 400
    if password == "":
      return {'Error':'Please input a valid password'}, 400
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
    else:
      return {'Error': 'Only admins are allowed to add users'}

  def get(self):
    create_admin()
    return users

class Login(Resource):
  """Endpoint to login a user and create an access token"""
  def post(self):
    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()

    user = find_user(username)
    if len(user) == 0:
      return {'Error':'Username does not exist'}, 404

    if password != user[0]['password']:
      return {'Error':'Wrong password'}, 401

    i_user = [user[0]['id'], user[0]['username'], user[0]['role']]
    access_token = create_access_token(identity=i_user)

    mesg = {
        'access_token': access_token,
        }
    return mesg, 200
