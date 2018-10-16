from flask_restful import Resource, reqparse

records = []

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('book_id', type=str, location='json')
class Records(Resource):
  """docstring for Records"""

  """ endpoint for POST requests to /dann/api/v1/records"""
  def post(self):
    args = parser.parse_args()

    new_sale = {
        'id': len(records) + 1,
        'details': "change this",
        'attendant': "dan"
    }
    records.append(new_sale)
    return {"message" : "Success! Sale recorded"}, 200
