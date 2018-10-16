from flask_restful import Resource, reqparse

records = []

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('book_id', type=str, location='json')
class SingleRecord(Resource):
  """docstring for SingleRecord"""

  """ endpoint for POST requests to /dann/api/v1/sales/<saleId>"""
  def get(self, saleID):
    record = [record for record in records if record['id'] == saleID]
    if len(record) == 0:
      return {'Error':'That sale record does not exist'}, 404
    return {'Sale': record[0]}, 200
