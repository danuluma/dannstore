from flask_restful import Resource, reqparse
import os
import sys
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

# local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v2.models.product import ProductModel
from app.api.v2.models.sales import SalesModel


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('books_id', action='append', type=int, location='json')


def attendant_sales(sales, user_id):
    """Return attendant sales"""

    for sale in sales:
        items = []
        if sale.get('created_by') == user_id:
            items.append(sale)
        if not items:
            return {"Error": "You don't have any sales"}, 404
        return {"Sales": items}, 200

class Records(Resource):
    """Maps to /sales"""

    @jwt_required
    def get(self):
        """ Endpoint for GET requests to /api/v2/sales"""

        current_user = get_jwt_identity()
        sales = SalesModel().get_all_sales()

        user_id = current_user[0]
        if not sales:
            return {"Error": "There are no sale records"}, 404
        if current_user[2] == "admin":
            return {"Sales": sales}, 200
        return attendant_sales(sales, user_id)

    @jwt_required
    def post(self):
        """ Endpoint for POST requests to /api/v2/sales"""

        args = parser.parse_args()
        books_id = args['books_id']
        total= 0
        for book in books_id:
            details = ProductModel().get_single_book(book, 0)
            if not details:
                return {"Error": f"Book {book} does not exist"}, 404
            total += details.get('price')

        current_user = get_jwt_identity()
        created_by = current_user[0]
        new_sale = [
            books_id,
            total,
            created_by
        ]
        if current_user[2] != "admin":
            SalesModel().add_new_record(new_sale)
            for book in books_id:
                ProductModel().sell_book(book, 1)
            return {"message": "Success! Sale recorded"}, 201
        return {"Error": "Only store attendants can create sale records"}, 403


class SingleRecord(Resource):
    """Maps to /sales/<saleId>"""

    @jwt_required
    def get(self, saleID):
        """ Endpoint for POST requests to /api/v2/sales/<saleId>"""

        record = SalesModel().get_single_sale(saleID, 0)
        if not record:
            return {'Error': 'That sale record does not exist'}, 404
        current_user = get_jwt_identity()
        user_role = current_user[2]
        user_id = current_user[0]
        sale_creator = record.get('created_by')
        if (user_role == "admin") or (user_id == sale_creator):
            return {'Sale': record}, 200
        return {"Error": "Only admins can access this"}, 403
