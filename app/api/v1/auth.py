from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token


users = [
]


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True, help='please enter a username',  location='json')
parser.add_argument('password', type=str, required=True, help='password can\'t be empty', location='json')
parser.add_argument('access_token', location='json')

def find_user(username):
  args = parser.parse_args()
  user = [user for user in users if user['username'] == username]
  return user

class Register(Resource):
  """Endpoint to register a new user"""
  def post(self):
    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()

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
            'password': password
            }
    users.append(new_user)
    return {'users': users}, 200

class Login(Resource):
  """Endpoint to login a user and create an access token"""
  def post(self):
    args = parser.parse_args()
    username = args['username'].strip()
    password = args['password'].strip()

    user = find_user(username)
    if len(user) == 0:
      return {'Error':'Username/Email does not exist'}, 404

    if password != user[0]['password']:
      return {'Error':'Wrong password'}, 401

    i_user = [user[0]['id'], user[0]['username']]
    access_token = create_access_token(identity=i_user)

    mesg = {
        'access_token': access_token,
        }
    return mesg, 200
