import json
import os
import sys
import unittest

# local

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.tests.v2.test_base import Apiv2Test


class SalesTest(Apiv2Test):
    """ Tests for apiv2 products endpoints """


    def test_get_empty_sales_record(self):
        """Tests /sales endpoint. There are no sales records yet"""
        access_token = self.get_token(self.test_owner)
        response = self.client().get(self.url + 'sales',
                                     headers={"Authorization": "Bearer " + access_token})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'), "There are no sale records")
        self.assertEqual(response.status_code, 404)

    def test_try_add_a_sales_record_as_admin(self):
        """Tests POST /sales endpoint. Only attendants can access this"""

        access_token = self.get_token(self.test_owner)
        self.client().post(self.url + 'products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        response = self.client().post(self.url + 'sales',
                                      headers={"Authorization": "Bearer " + access_token}, json={'books_id': [1]})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'),
                         "Only store attendants can create sale records")
        self.assertEqual(response.status_code, 403)

    def test_add_a_sales_record_as_attendant(self):
        """Tests POST /sales endpoint. Only attendants can access this"""

        access_token = self.get_token(self.test_owner)
        self.client().post(self.url + 'products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        access_token = self.get_token(self.test_user)
        response = self.client().post(self.url + 'sales',
                                      headers={"Authorization": "Bearer " + access_token}, json={'books_id': [1]})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('message'))
        self.assertEqual(json_data.get('message'), "Success! Sale recorded")
        self.assertEqual(response.status_code, 201)

    def test_sell_invalid_product(self):
        """Tests POST /sales endpoint. Only attendants can access this"""

        access_token = self.get_token(self.test_owner)
        self.client().post(self.url + 'products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        access_token = self.get_token(self.test_user)
        response = self.client().post(self.url + 'sales',
                                      headers={"Authorization": "Bearer " + access_token}, json={'books_id': [11]})
        json_data = json.loads(response.data)
        print(json_data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'), "Book with id 11 does not exist")
        self.assertEqual(response.status_code, 404)

    def test_get_all_sales_record_as_admin(self):
        """Tests /sales endpoint."""

        access_token = self.get_token(self.test_owner)
        self.client().post(self.url + 'products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        access_token = self.get_token(self.test_user)
        self.client().post(self.url + 'sales',
                           headers={"Authorization": "Bearer " + access_token}, json={'books_id': [1]})
        access_token = self.get_token(self.test_owner)
        response = self.client().get(self.url + 'sales',
                                     headers={"Authorization": "Bearer " + access_token})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Sales'))
        self.assertEqual(response.status_code, 200)

    def test_get_sales_record_as_attendant(self):
        """Tests /sales endpoint."""

        access_token = self.get_token(self.test_owner)
        self.client().post(self.url + 'products',
                           headers={"Authorization": "Bearer " + access_token}, json=self.test_book)
        access_token = self.get_token(self.test_user)
        self.client().post(self.url + 'sales',
                           headers={"Authorization": "Bearer " + access_token}, json={'books_id': [1]})
        response = self.client().get(self.url + 'sales',
                                     headers={"Authorization": "Bearer " + access_token})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Sales'))
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_sale(self):
        """Tests /sales/<saleId> endpoint. There are no sales records yet"""

        access_token = self.get_token(self.test_owner)
        response = self.client().get(self.url + 'sales/0',
                                     headers={"Authorization": "Bearer " + access_token})
        json_data = json.loads(response.data)
        self.assertTrue(json_data.get('Error'))
        self.assertEqual(json_data.get('Error'),
                         "That sale record does not exist")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
