from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
)
import os, sys



# Local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.product import ProductModel

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'title', type=str, help='enter the book\'s name', location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument(
    'price', type=int, help='price of the book', location='json')
parser.add_argument('quantity', type=int, help='how many?', location='json')
parser.add_argument('minimum', type=int,
                    help='minimun required', location='json')
parser.add_argument('image_url', type=str,
                    help='url to the book\'s image', location='json')



def find_book(param, which_row):
  """Finds and returns a book by supplied param."""

  args = parser.parse_args()
  book = ProductModel().get_single_book(param, which_row)
  return book



def add_product(new_book):
  """Adds a new book"""

  try:
        ProductModel().add_new_book(new_book)
  except:
    return {"Error":"Title already exists"}, 409
  return {'Message': "Success! Book added"}, 201


class Products(Resource):
  """Maps to /products endpoint"""


  @jwt_required
  def get(self):
    """ Returns all books in the database"""
    books = ProductModel().get_all_books()
    return books, 200



  @jwt_required
  def post(self):
    """Endpoint to add a new book"""

    args = parser.parse_args()
    title = args['title'].strip()
    description = args['description'].strip()
    price = args['price']
    quantity = args['quantity']
    minimum = args['minimum']
    image_url = args['image_url'].strip()

    user = find_book(title, 1)

    if user:
      return {'Error': 'Title already exists'}, 409

    current_user = get_jwt_identity()
    role = current_user[2]
    my_id = current_user[0]
    new_book = [
        title,
        description,
        price,
        quantity,
        minimum,
        image_url,
        my_id
    ]

    if role == 0:
      return add_product(new_book)
    return {'Error': 'Only admins are allowed to add new books'}, 401
