import os
import sys
import unittest
import json

#local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v1.auth import create_admin, clear_users
from app.api.v1.products_view import clear_books
from app.api.v1.sales_view import clear_records


class SalesTest(unittest.TestCase):
  """ Tests for api /recordss endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.test_user = {"username": "dan", "password": "dann", "role": 2}
    self.test_admin = {"username": "owner", "password": "secret"}
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
    clear_records()
    clear_users()
    clear_books()


  def test_get_sales_record_without_admin_rights(self):
    """Tests /sales endpoint. One has to be an admin to access"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v1/sales', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only admins are allowed to view all sales records")
    self.assertEqual(response.status_code, 401)

  def test_get_empty_sales_record(self):
    """Tests /sales endpoint. There are no sales records yet"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v1/sales', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "There are no sale records")
    self.assertEqual(response.status_code, 404)

  def test_try_add_a_sales_record_as_admin(self):
    """Tests POST /sales endpoint. Only attendants can access this"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().post('/dann/api/v1/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id':1})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only store attendants can create sale records")
    self.assertEqual(response.status_code, 401)

  def test_add_a_sales_record_as_attendant(self):
    """Tests POST /sales endpoint. Only attendants can access this"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v1/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id':1})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Success! Sale recorded")
    self.assertEqual(response.status_code, 200)

  def test_get_sales_record(self):
    """Tests /sales endpoint."""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    self.client().post('/dann/api/v1/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v1/login', json=self.test_user)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    self.client().post('/dann/api/v1/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id': 1})
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v1/sales', headers={"Authorization": "Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Sales'))
    self.assertEqual(response.status_code, 200)

  def test_get_non_existent_sale(self):
    """Tests /sales/<saleId> endpoint. There are no sales records yet"""
    create_admin()
    response = self.client().post('/dann/api/v1/login', json=self.test_admin)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().get('/dann/api/v1/sales/0', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "That sale record does not exist")
    self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
  unittest.main()
