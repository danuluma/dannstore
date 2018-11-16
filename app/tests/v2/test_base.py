import json
import os
import sys
import unittest

# local

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from run import create_app
from app.api.v2.db import Db


class Apiv2Test(unittest.TestCase):
    """ Tests for api v2 endpoints """

    def setUp(self):
        """Run this before each test"""

        self.app = create_app("testing")
        self.client = self.app.test_client
        self.url = '/api/v2/'
        self.test_user = {"username": "dancan",
                          "password": "Admintest1"}
        self.test_owner = {"username": "owner",
                           "password": "secret1"}
        self.test_book = {
            "title": "test_book2",
            "description": "An awesome read",
            "category": "fiction",
            "price": 100,
            "quantity": 5,
            "minimum": 4,
            "image_url": "url",
            "created_by": 0
        }

        with self.app.app_context():
            # Db().drop()
            Db().create()

    def tearDown(self):
        """Run this after each test"""

        with self.app.app_context():
            Db().drop()

    def get_token(self, user):
        """Return an access token"""

        response = self.client().post(self.url + 'login', json=self.test_owner)
        json_data = json.loads(response.data)
        access_token = json_data.get('access_token')
        self.client().post(self.url + 'signup',
                           headers={"Authorization": "Bearer " + access_token},
                           json=user)
        response = self.client().post(self.url + 'login',
                                      headers={
                                          "Authorization": "Bearer " + access_token},
                                      json=user)
        json_data = json.loads(response.data)
        user_token = json_data.get('access_token')
        return user_token


if __name__ == '__main__':
    unittest.main()
