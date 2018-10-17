from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

books = []


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', type=str, help='enter the book\'s name', location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument('price', type=int, help='price of the book', location='json')
parser.add_argument('quantity', type=int, help='how many?', location='json')
parser.add_argument('minimun', type=int, help='minimun required', location='json')
parser.add_argument('image_url', type=str, help='url to the book\'s image', location='json')

def clear_books():
  """Clears the books list"""

  books.clear()


class Home(Resource):
  """Just a test endpoint ~/dann/api/v1/home"""

  def get(self):
    return {"message": "Hello, there ;-)"}, 200


class Products(Resource):
  """Maps to /products endpoint"""

  def get(self):
    """ endpoint for GET requests to /dann/api/v1/products"""

    if len(books) != 0:
      return {"Books" : books}, 200
    else:
      return {"Error": "There are no books"}, 404

  @jwt_required
  def post(self):
    """ endpoint for POST requests to /dann/api/v1/products"""
    """ adds a new book"""

    args = parser.parse_args()
    book = [book for book in books if book['title'] == args['title']]
    if len(book) != 0:
      return {'Error':'Book already exists'}, 409
    if args['title'].strip() == "":
      return {'Error':'A book must have a valid title'}, 400
    new_book = {
        'id': len(books) + 1,
        'title': args['title'],
        'description': args['description'],
        'price': args['price'],
        'quantity': args['quantity'],
        'minimun': args['minimun'],
        'image_url': args['image_url']
    }
    current_user = get_jwt_identity()
    if current_user[2] == 0:
      books.append(new_book)
      return {'message': 'Success! Book added'}, 200
    return {"Error": "Only Admins are allowed to add books"}, 401
