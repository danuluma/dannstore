import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db



def format_user(user):
  details = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "role": user[3],
            "created_by": user[4],
            "created_at": str(user[5])
      }
  return details


class UserModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_users(self):
    userlist = []
    for user in Db().get_query('users'):
      details = format_user(user)
      userlist.append(details)
    return userlist

  def get_single_user(self, username):
    users = [row for row in Db().get_query('users') if row[1] == username]
    if users :
      user = users[0]
      return format_user(user)

  def add_new_user(self, user):
    Db().post_query("""
    INSERT INTO users (username, password, created_by)
    VALUES (%s,%s,%s);
    """, user)

