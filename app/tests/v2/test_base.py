import json
import os
import sys
import unittest
from dotenv import load_dotenv

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.db import Db

class Apiv2Test(unittest.TestCase):
  """ Tests for api v2 endpoints """

  def setUp(self):
    self.app = create_app("testing")
    self.client = self.app.test_client
    self.test_user = { "username": "dancan",
                        "password": "Admintest1"}
    self.test_owner = { "username": "owner",
                        "password": "secret1"}

    with self.app.app_context():
      Db().drop()
      Db().create()


  def tearDown(self):
    with self.app.app_context():
      Db().drop()
      Db().create()

if __name__ == '__main__':
  unittest.main()