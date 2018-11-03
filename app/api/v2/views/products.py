from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
)
import os
import sys


# Local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.product import ProductModel

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'title', type=str, help='enter the book\'s name', location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument('category', type=str, location='json')
parser.add_argument(
    'price', type=int, help='price of the book', location='json')
parser.add_argument('quantity', type=int, help='how many?', location='json')
parser.add_argument('minimum', type=int,
                    help='minimun required', location='json')
parser.add_argument('image_url', type=str,
                    help='url to the book\'s image', location='json')


def add_product(new_book):
    """Adds a new book"""


class Products(Resource):
    """Maps to /products endpoint"""

    @jwt_required
    def get(self):
        """ Returns all books in the database"""
        books = ProductModel().get_all_books()
        if books:
            return books, 200
        return {"Error": "No products available"}, 404

    @jwt_required
    def post(self):
        """Endpoint to add a new book"""

        args = parser.parse_args()
        title = args['title'].strip()
        description = args['description'].strip()
        category = args['category'].strip()
        price = args['price']
        quantity = args['quantity']
        minimum = args['minimum']
        image_url = args['image_url'].strip()

        book = ProductModel().get_single_book(title, 1)

        if book:
            return {'Error': 'Title already exists'}, 409

        if quantity < 1:
            return {'Error': 'Quantity can\'t be less than one'}, 400

        current_user = get_jwt_identity()
        # return current_user
        role = current_user[2]
        my_id = current_user[0]
        new_book = [
            title,
            description,
            category,
            price,
            quantity,
            minimum,
            image_url,
            my_id
        ]

        if role == 'admin':
            ProductModel().add_new_book(new_book)
            return {'Message': "Success! Book added"}, 201
        return {'Error': 'Only admins are allowed to add new books'}, 403


class SingleProduct(Resource):
    """Maps to /product/productID"""

    @jwt_required
    def get(self, productID):
        """Retrieves a single product by its ID"""

        book = ProductModel().get_single_book(productID, 0)
        return book, 200

    @jwt_required
    def put(self, productID):
        """Endpoint to edit a book."""

        args = parser.parse_args()
        title = args['title'].strip()
        description = args['description'].strip()
        category = args['category'].strip()
        price = args['price']
        quantity = args['quantity']
        minimum = args['minimum']
        image_url = args['image_url'].strip()

        book = ProductModel().get_single_book(productID, 0)

        if not book:
            return {'Error': 'Book by that ID does not exists'}, 404

        current_user = get_jwt_identity()
        # return current_user
        role = current_user[2]
        my_id = current_user[0]
        new_book = [
            title,
            description,
            category,
            price,
            quantity,
            minimum,
            image_url,
            my_id
        ]

        if role == 'admin':

            try:
                ProductModel().edit_book(productID, new_book)
            except:
                return {"Error": "Error"}, 404
            return {'Message': "Success! Book details updated!"}, 201
        return {"Error": "Only an admin can edit a book"}, 403

    @jwt_required
    def delete(self, productID):
        """Retrieves a single product by its ID"""

        current_user = get_jwt_identity()
        role = current_user[2]
        if role == 'admin':
            ProductModel().delete_book(productID)
            return {'Message': "Success! Book deleted"}, 200
        return {"Error": "Only admins can delete books"}, 403
