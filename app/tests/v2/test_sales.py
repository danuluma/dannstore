import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.tests.v2.test_base import Apiv2Test

class SalesTest(Apiv2Test):
  """ Tests for apiv2 products endpoints """


  def owner_token(self):
    """Get admin(owner) token."""

    response = self.client().post('/dann/api/v2/login', json=self.test_owner)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    return access_token

  def attendant_token(self):
    """Get attendant token."""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    att_access_token = json_data.get('access_token')
    return att_access_token


  def test_get_sales_record_without_admin_rights(self):
    """Tests /sales endpoint. One has to be an admin to access"""
    access_token = self.attendant_token()
    response = self.client().get('/dann/api/v2/sales', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only admins are allowed to view all sales records")
    self.assertEqual(response.status_code, 401)

  def test_get_empty_sales_record(self):
    """Tests /sales endpoint. There are no sales records yet"""
    access_token = self.owner_token()
    response = self.client().get('/dann/api/v2/sales', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "There are no sale records")
    self.assertEqual(response.status_code, 404)

  def test_try_add_a_sales_record_as_admin(self):
    """Tests POST /sales endpoint. Only attendants can access this"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().post('/dann/api/v2/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id':1})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only store attendants can create sale records")
    self.assertEqual(response.status_code, 401)

  def test_add_a_sales_record_as_attendant(self):
    """Tests POST /sales endpoint. Only attendants can access this"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    access_token = self.attendant_token()
    response = self.client().post('/dann/api/v2/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id':1})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Success! Sale recorded")
    self.assertEqual(response.status_code, 201)

  def test_get_sales_record(self):
    """Tests /sales endpoint."""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    access_token = self.attendant_token()
    self.client().post('/dann/api/v2/sales', headers={"Authorization":"Bearer " + access_token}, json={'book_id': 1})
    access_token = self.owner_token()
    response = self.client().get('/dann/api/v2/sales', headers={"Authorization": "Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Sales'))
    self.assertEqual(response.status_code, 200)

  def test_get_non_existent_sale(self):
    """Tests /sales/<saleId> endpoint. There are no sales records yet"""

    access_token = self.owner_token()
    response = self.client().get('/dann/api/v2/sales/0', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "That sale record does not exist")
    self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
  unittest.main()
