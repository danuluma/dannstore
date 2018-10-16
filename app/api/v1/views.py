from flask_restful import Resource

products = [{
        'id': 1,
        'title': "Coming soon",
        'description': "LOrem ipsum",
        'price': 100,
        'quantity': 20,
        'minimun': 5,
        'image_url':'coming_soon'
    }]

class Home(Resource):
  """Just a test endpoint ~/dann/api/v1/home"""
  def get(self):
    return {"message": "Hello, there ;-)"}, 200


class Products(Resource):
  """docstring for Products"""
  """ endpoint for GET requests to /dann/api/v1/products"""
  def get(self):
    if len(products) != 0:
      return {"Books" : products}, 200
    else:
      return {"Error": "There are no books"}, 404
