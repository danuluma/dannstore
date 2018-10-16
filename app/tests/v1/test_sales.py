import os
import sys
import unittest
import json

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app


class SalesTest(unittest.TestCase):
  """ Tests for api /recordss endpoints """

  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client

  def tearDown(self):
    pass


  def test_get_empty_sales_record(self):
    """Tests /sales endpoint. There are no sales records yet"""
    response = self.client().get('/dann/api/v1/sales')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "There are no sale records")
    self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
  unittest.main()
