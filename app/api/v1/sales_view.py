from flask_restful import Resource, reqparse
import os
import sys
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

# local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v1.products_view import books


records = []

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('book_id', type=int, location='json')


def clear_records():
    """Clears the books list"""

    records.clear()


class Records(Resource):
    """Maps to /sales"""

    @jwt_required
    def get(self):
        """ endpoint for GET requests to /api/v1/sales"""

        current_user = get_jwt_identity()
        if current_user[2] == 'admin':
            if len(records) == 0:
                return {"Error": "There are no sale records"}, 404
            return {"Sales": records}, 200
        return {"Error": "Only admins are allowed to view all sales records"}, 403

    @jwt_required
    def post(self):
        """ endpoint for POST requests to /api/v1/sales"""

        args = parser.parse_args()
        book = [book for book in books if book['id'] == args['book_id']]
        current_user = get_jwt_identity()
        new_sale = {
            'id': len(records) + 1,
            'details': book,
            'attendant': current_user[1],
            'att_id': current_user[0]
        }
        if current_user[2] != 'admin':
            if len(book) != 0:
                records.append(new_sale)
                return {"message": "Success! Sale recorded"}, 201
            return {"Error": "That book does not exist"}, 404
        return {"Error": "Only store attendants can create sale records"}, 403


class SingleRecord(Resource):
    """Maps to /sales/<saleId>"""

    @jwt_required
    def get(self, saleID):
        """ endpoint for POST requests to /api/v1/sales/<saleId>"""

        record = [record for record in records if record['id'] == saleID]
        current_user = get_jwt_identity()
        if len(record) == 0:
            return {'Error': 'That sale record does not exist'}, 404
        if (current_user[2] == 'admin') or (current_user[0] == record[3]):
            return {'Sale': record[0]}, 200
        return {"Error": "Only admins can access this"}, 403
