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
from app.tests.v2.test_base import Apiv2Test

class UsersTest(Apiv2Test):
  """ Tests for api v2 endpoints """


  def owner_token(self):
    response = self.client().post('/dann/api/v2/login', json=self.test_owner)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    return access_token

  def test_owner_login(self):
    """Default owner login."""

    response = self.client().post('/dann/api/v2/login', json=self.test_owner)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)


  def test_user_reg(self):
    """ Test user registration with valid credentials """


    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 201)

  def test_duplicate_user_reg(self):
    """ Test user registration with valid credentials """

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertEqual(response.status_code, 409)

  def test_user_reg_with_no_username(self):
    """ Test user registration with null username """

    test_user2 = { "username": "", "password": "Admintest1"}
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=test_user2)
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_no_password(self):
    """ test user registration with null password """

    test_user3 = { "username": "dann", "password": ""}
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=test_user3)
    self.assertEqual(response.status_code, 400)

  # def test_user_login(self):
  #   """ test user login """

  #   test_user5 = { "username": "dann2", "password": "Admintest1"}
  #   response = self.client().post('/dann/api/v2/login', json=self.test_owner)
  #   json_data = json.loads(response.data)
  #   access_token = json_data.get('access_token')
  #   self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=test_user5)
  #   json_data = json.loads(response.data)
  #   print(json_data)
  #   response = self.client().post('/dann/api/v2/login', json=test_user5)
  #   json_data = json.loads(response.data)
  #   print(json_data)
  #   self.assertTrue(json_data.get('access_token'))
  #   self.assertEqual(response.status_code, 200)

  def test_user_login_with_wrong_password(self):
    """ test user login with wrong password """

    test_user4 = { "username": "dancan",
                        "password": "wrong"}
    response = self.client().post('/dann/api/v2/login', json=self.test_owner)
    json_data = json.loads(response.data)
    access_token = json_data.get('access_token')
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=test_user4)
    self.assertNotEqual(response.status_code, 200)

  def test_user_login_with_wrong_username(self):
    """ test user login with wrong username """
    test_user4 = { "username": "wrong",
                        "password": "Admintest1"}
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/reg', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=test_user4)
    self.assertNotEqual(response.status_code, 200)

  def test_access_protected_endpoint_without_authorization(self):
    response = self.client().post('/dann/api/v2/reg')
    self.assertNotEqual(response.status_code, 403)

if __name__ == '__main__':
  unittest.main()