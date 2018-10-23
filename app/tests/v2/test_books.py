import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.db import Db
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

    book4 = {
            "title": "test_book4",
            "description": "An awesome read",
            "price": 100,
            "quantity": 5,
            "minimum": 4,
            "image_url": "url",
            "created_by": 0
            }
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=book4)
    json_data = json.loads(response.data)
    print(json_data)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Success! Book added")
    self.assertEqual(response.status_code, 201)

  def test_get_all_books_as_owner(self):
    """Test retrieve all books with admin rights"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token}, json=self.test_book)
    response = self.client().get('/dann/api/v2/products', headers={"Authorization":"Bearer " + access_token})
    self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
  unittest.main()
