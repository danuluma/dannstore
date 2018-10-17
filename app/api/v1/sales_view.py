from flask_restful import Resource

records = []


class Records(Resource):
  """Maps to /sales"""

  def get(self):
    """ endpoint for GET requests to /dann/api/v1/sales"""
    if len(records) == 0:
      return {"Error": "There are no sale records"}, 404
    return {"Sales" : records}, 200
