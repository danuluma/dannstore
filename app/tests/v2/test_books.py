import json
import os
import sys
import unittest

# local

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.tests.v2.test_base import Apiv2Test


class ProductsTest(Apiv2Test):
    """ Tests for apiv2 products endpoints """


    def test_add_book(self):
        """ Test adding with a book valid credentials """

        access_token = self.owner_token()
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Message'))
        self.assertEqual(json_data.get('Message'), "Success! Book added")
        self.assertEqual(response.status_code, 201)

    def test_try_add_book_without_admin_rights(self):
        """ Test adding with a book invalid credentials """

        access_token = self.attendant_token()
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'),
                         "Only admins are allowed to add new books")
        self.assertEqual(response.status_code, 403)

    def test_try_add_a_duplicate_book(self):
        """ Test adding a book that already exists """

        access_token = self.owner_token()
        self.client().post('/api/v2/products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().post('/api/v2/products',
                                      headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'), "Title already exists")
        self.assertEqual(response.status_code, 409)

    def test_get_all_books(self):
        """Test retrieve all books"""

        access_token = self.owner_token()
        self.client().post('/api/v2/products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().get('/api/v2/products',
                                     headers={"Authorization": "Bearer " + access_token})
        self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        """ Test adding with a book valid credentials """

        book3 = {

            "title": "book3",
            "description": "Another awesome read",
            "category": "fiction",
            "price": 110,
            "quantity": 50,
            "minimum": 4,
            "image_url": "new_url",
            "updated_by": 0
        }
        access_token = self.owner_token()
        self.client().post('/api/v2/products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().put('/api/v2/products/1',
                                     headers={"Authorization": "Bearer " + access_token}, json=book3)
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Message'))
        self.assertEqual(json_data.get('Message'),
                         "Success! Book details updated!")
        self.assertEqual(response.status_code, 201)

    def test_delete_a_book(self):
        """Delete a user as the owner"""

        access_token = self.owner_token()
        self.client().post('/api/v2/products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().delete('/api/v2/products/1',
                                        headers={"Authorization": "Bearer " + access_token})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Message'))
        self.assertEqual(json_data.get('Message'), "Success! Book deleted")
        self.assertEqual(response.status_code, 200)

    def test_try_delete_a_book_without_admin_rights(self):
        """Try to delete a book without admin rights"""

        access_token = self.attendant_token()
        self.client().post('/api/v2/products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().delete('/api/v2/products/1',
                                        headers={"Authorization": "Bearer " + access_token}, json={"user_id": 1})
        json_data = json.loads(response.data)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'),
                         "Only admins can delete books")
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
