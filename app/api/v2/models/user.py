import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class UserModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_users(self):
    return Db().get_query('users')

  def add_new_user(self, user):
    Db().post_query("""
    INSERT INTO users (username, password, created_by)
    VALUES (%s,%s,%s);
    """, user)

