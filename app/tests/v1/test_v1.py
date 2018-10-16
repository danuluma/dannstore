import os
import sys
import unittest
import json

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app


class Apiv1Test(unittest.TestCase):
  """ Tests for api endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.test_book = {
        'id': 1,
        'title': "Coming soon",
        'description': "LOrem ipsum",
        'price': 100,
        'quantity': 20,
        'minimun': 5,
        'image_url':'coming_soon'
    }

  def tearDown(self):
    pass


  def test_home(self):
    """Tests the home endpoint"""
    response = self.client().get('/dann/api/v1/home')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Hello, there ;-)")
    self.assertEqual(response.status_code, 200)

  def test_get_empty_product_list(self):
    """Tests GET /products endpoint. There are no items yet"""
    response = self.client().get('/dann/api/v1/products')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "There are no books")
    self.assertEqual(response.status_code, 404)

  def test_add_new_book(self):
    """Tests POST /products endpoint. Adds a new book"""
    response = self.client().post('/dann/api/v1/products', json=self.test_book)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Success! Book added")
    self.assertEqual(response.status_code, 200)

  def test_get_all_books(self):
    """Tests GET /products endpoint. There are no items yet"""
    self.client().post('/dann/api/v1/products', json=self.test_book)
    response = self.client().get('/dann/api/v1/products')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Books'))
    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
  unittest.main()
