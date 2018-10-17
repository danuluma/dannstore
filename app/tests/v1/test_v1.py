import os
import sys
import unittest
import json

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v1.auth import create_admin, clear_users
from app.api.v1.views import clear_books



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
    self.test_user = {"username": "dan", "password": "dann", "role": 2}
    self.test_admin = {"username": "owner", "password": "secret"}

  def tearDown(self):
    clear_users()
    clear_books()


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
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Success! Book added")
    self.assertEqual(response.status_code, 200)

  def test_add_duplicate_book(self):
    """Tests POST /products endpoint. Adds a new book"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Book already exists")
    self.assertEqual(response.status_code, 409)

  def test_try_add_new_book_while_unauthorized(self):
    """Tests POST /products endpoint. Tries to add a new book without admin rights"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only Admins are allowed to add books")
    self.assertEqual(response.status_code, 401)

  def test_get_all_books(self):
    """Tests GET /products endpoint."""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().get('/dann/api/v1/products')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Books'))
    self.assertEqual(response.status_code, 200)

  def test_get_a_book_by_id(self):
    """Tests GET /products endpoint."""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().get('/dann/api/v1/products/1')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Book'))
    self.assertEqual(response.status_code, 200)

  def test_get_non_existent_book_by_id(self):
    """Tests /products/productID endpoint. There are no items yet"""
    response = self.client().get('/dann/api/v1/products/0')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "That book does not exist")
    self.assertEqual(response.status_code, 404)


  def test_login_as_owner(self):
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)

  def test_register_new_attendant(self):
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Success!")
    self.assertEqual(response.status_code, 200)

  def test_register_duplicate_attendant(self):
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Username already exists")
    self.assertEqual(response.status_code, 409)

if __name__ == '__main__':
  unittest.main()
