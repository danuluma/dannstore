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
parser.add_argument('book_id', type=int, location='json')


class Records(Resource):
  """Maps to /sales"""

  @jwt_required
  def get(self):
    """ endpoint for GET requests to /dann/api/v2/sales"""

    current_user = get_jwt_identity()
    if current_user[2] == 0:
      sales = SalesModel().get_all_sales()
      if len(sales) == 0:
        return {"Error": "There are no sale records"}, 404
      return {"Sales": sales}, 200
    return {"Error": "Only admins are allowed to view all sales records"}, 401

  @jwt_required
  def post(self):
    """ endpoint for POST requests to /dann/api/v2/sales"""

    args = parser.parse_args()
    book_id = args['book_id']
    details = ProductModel().get_single_book(book_id, 0)
    total = details.get('price')
    book_id = details.get('id')
    current_user = get_jwt_identity()
    created_by = current_user[0]
    new_sale = [
         book_id,
         total,
         created_by
    ]
    if current_user[2] != 0:
      if len(details) != 0:
        SalesModel().add_new_record(new_sale)
        return {"message": "Success! Sale recorded"}, 201
      return {"Error": "That book does not exist"}, 404
    return {"Error": "Only store attendants can create sale records"}, 401


class SingleRecord(Resource):
  """Maps to /sales/<saleId>"""

  @jwt_required
  def get(self, saleID):
    """ Endpoint for POST requests to /dann/api/v2/sales/<saleId>"""

    record = SalesModel().get_single_sale(saleID, 0)
    current_user = get_jwt_identity()
    if not record:
      return {'Error': 'That sale record does not exist'}, 404
    if (current_user[2] == 0) or (current_user[0] == record[3]):
      return {'Sale': record[0]}, 200
    return {"Error": "Only admins can access this"}, 401
