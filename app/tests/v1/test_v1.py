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

  def tearDown(self):
    pass


  def test_home(self):
    """Tests the home endpoint"""
    response = self.client().get('/dann/api/v1/home')
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('message'))
    self.assertEqual(json_data.get('message'), "Hello, there ;-)")
    self.assertEqual(response.status_code, 200)
    print("yes")

if __name__ == '__main__':
  unittest.main()
