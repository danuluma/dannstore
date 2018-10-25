import json
import os
import sys
import unittest

#local
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.tests.v2.test_base import Apiv2Test

class UsersTest(Apiv2Test):
  """ Tests for api v2 endpoints """


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

  def test_owner_login(self):
    """Default owner login."""

    response = self.client().post('/dann/api/v2/login', json=self.test_owner)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)


  def test_user_reg(self):
    """ Test user registration with valid credentials """

    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Success! User created")
    self.assertEqual(response.status_code, 201)

  def test_duplicate_user_reg(self):
    """ Test user registration with valid credentials """

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Username already exists")
    self.assertEqual(response.status_code, 409)

  def test_user_reg_with_invalid_username(self):
    """ Test user registration with null username """

    test_user2 = { "username": "", "password": "Admintest1"}
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=test_user2)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Please input a valid username")
    self.assertEqual(response.status_code, 400)

  def test_user_reg_with_invalid_password(self):
    """ test user registration with null password """

    test_user3 = { "username": "dann", "password": ""}
    access_token = self.owner_token()
    response = self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=test_user3)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Please input a valid password")
    self.assertEqual(response.status_code, 400)

  def test_user_login(self):
    """ test user login """

    test_user5 = { "username": "dann79", "password": "Admintest1"}
    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization": "Bearer " + access_token}, json=test_user5)
    response = self.client().post('/dann/api/v2/login', json=test_user5)
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('access_token'))
    self.assertEqual(response.status_code, 200)

  def test_user_login_with_wrong_password(self):
    """ test user login with wrong password """

    test_user4 = { "username": "dancan",
                        "password": "wrong"}
    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=test_user4)
    json_data = json.loads(response.data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Wrong password or username")
    self.assertEqual(response.status_code, 400)


  def test_user_login_with_wrong_username(self):
    """ test user login with wrong username """

    test_user4 = { "username": "wrong",
                        "password": "Admintest1"}
    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().post('/dann/api/v2/login', json=test_user4)
    json_data = json.loads(response.data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Wrong password or username")
    self.assertEqual(response.status_code, 400)


  def test_access_protected_endpoint_without_authorization(self):
    """Test access to a protected endpoint without logging in"""

    response = self.client().post('/dann/api/v2/signup')
    json_data = json.loads(response.data)
    print(json_data)
    self.assertNotEqual(response.status_code, 201)

  def test_get_all_users_as_owner(self):
    """Test retrieve all users with admin rights"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().get('/dann/api/v2/users', headers={"Authorization":"Bearer " + access_token})
    self.assertEqual(response.status_code, 200)


  def test_try_get_all_users_as_attendant(self):
    """Test retrieve all users without admin rights"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    access_token = self.attendant_token()
    response = self.client().get('/dann/api/v2/users', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only admins can view all users")
    self.assertEqual(response.status_code, 401)


  def test_get_single_users_as_owner(self):
    """Test retrieve a single user by id with admin rights"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().get('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token})
    self.assertEqual(response.status_code, 200)

  def test_try_get_single_users_as_attendant(self):
    """Test retrieve a single user by id without admin rights"""

    access_token = self.attendant_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().get('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only admins can view other users")
    self.assertEqual(response.status_code, 401)

  def test_promote_user(self):
    """Test promote user as the owner."""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().put('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token}, json={"action":"promote"})
    json_data = json.loads(response.data)
    print(json_data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Success! User promoted to an admin")
    self.assertEqual(response.status_code, 201)


  def test_promote_fellow_user(self):
    """Try promote another user as an attendant"""

    access_token = self.attendant_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().put('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token}, json={"action":"promote"})
    json_data = json.loads(response.data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only the owner can promote or demote")
    self.assertEqual(response.status_code, 401)

  def test_delete_a_user(self):
    """Delete a user as the owner"""

    access_token = self.owner_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().delete('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Success! That user has been deleted")
    self.assertEqual(response.status_code, 201)


  def test_try_delete_a_fellow_user(self):
    """Try to delete a user without admin rights"""

    access_token = self.attendant_token()
    self.client().post('/dann/api/v2/signup', headers={"Authorization":"Bearer " + access_token}, json=self.test_user)
    response = self.client().delete('/dann/api/v2/users/1', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertNotEqual(response.status_code, 200)
    self.assertTrue(json_data.get('Error'))
    self.assertEqual(json_data.get('Error'), "Only the owner can delete attendants")
    self.assertEqual(response.status_code, 401)

  def test_user_logout(self):
    access_token = self.owner_token()
    response = self.client().delete('/dann/api/v2/logout', headers={"Authorization":"Bearer " + access_token})
    json_data = json.loads(response.data)
    self.assertTrue(json_data.get('Message'))
    self.assertEqual(json_data.get('Message'), "Successfully logged out")
    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
  unittest.main()
