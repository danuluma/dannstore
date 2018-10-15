from flask_restful import Resource


class Home(Resource):
  """Just a test endpoint ~/dann/api/v1/home"""
  def get(self):
    return {"message": "Hello, there ;-)"}, 200

