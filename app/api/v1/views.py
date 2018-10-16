from flask_restful import Resource, reqparse

books = [{"id":1}]

class Home(Resource):
  """Just a test endpoint ~/dann/api/v1/home"""
  def get(self):
    return {"message": "Hello, there ;-)"}, 200


class Products(Resource):
  """docstring for Products"""
  """ endpoint for GET requests to /dann/api/v1/products"""
  def get(self):
    if len(books) != 0:
      return {"Books" : books}, 200
    else:
      return {"Error": "There are no books"}, 404

class SingleProduct(Resource):
  """docstring for SingleProduct"""
  """ endpoint for GET requests to /dann/api/v1/products/<productID>"""
  def get(self, productID):
    book = [book for book in books if book['id'] == productID]
    if len(book) == 0:
      return {'Error':'That book does not exist'}, 404
    return {'order': book[0]}, 200
