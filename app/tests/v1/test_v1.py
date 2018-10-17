import os
import sys
import unittest
import json

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v1.auth import create_admin, clear_users



class Apiv1Test(unittest.TestCase):
  """ Tests for api endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.test_user = {"username": "dan", "password": "dann", "role": 1}
    self.test_admin = {"username": "owner", "password": "secret"}

  def tearDown(self):
    clear_users()


  def test_home(self):
    """Tests the home endpoint"""
    response = self.client().get('/dann/api/v1/home')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Hello, there ;-)")
    self.assertEqual(response.status_code, 200)

  def test_get_empty_product_list(self):
    """Tests /products endpoint. There are no items yet"""
    response = self.client().get('/dann/api/v1/products')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "There are no books")
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
