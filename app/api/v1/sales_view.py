from flask_restful import Resource

records = []


class Records(Resource):
  """docstring for Records"""
  """ endpoint for GET requests to /dann/api/v1/records"""
  def get(self):
    if len(records) == 0:
      return {"Error": "There are no sale records"}, 404
    return {"Sales" : records}, 200
