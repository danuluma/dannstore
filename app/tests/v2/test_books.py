import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.tests.v2.test_base import Apiv2Test

class ProductsTest(Apiv2Test):
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
    self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    att_access_token = json_data.get('access_token')
    return att_access_token


  def test_add_book(self):
    """ Test adding with a book valid credentials """

    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    print(json_data)
    print(access_token)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Success! Book added")
    self.assertEqual(response.status_code, 201)

  def test_try_add_book_without_admin_rights(self):
    """ Test adding with a book invalid credentials """

    access_token = self.attendant_token()
    response = self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only admins are allowed to add new books")
    self.assertEqual(response.status_code, 401)

  def test_try_add_a_duplicate_book(self):
    """ Test adding a book that already exists """

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Title already exists")
    self.assertEqual(response.status_code, 409)

  def test_get_all_books(self):
    """Test retrieve all books"""

    access_token = self.attendant_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().get('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token})
    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
  unittest.main()
