import os
import sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


def format_user(user):
    """Formats the results to a dictionary"""

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
    """User Model. User stuff here"""

    def get_all_users(self):
        """Gets all users from the db"""

        userlist = []
        for user in Db().get_query('users'):
            details = format_user(user)
            userlist.append(details)
        return userlist

    def get_single_user(self, param, this_row):
        """Gets a single user"""

        users = [row for row in Db().get_query(
            'users') if row[this_row] == param]
        if users:
            user = users[0]
            return format_user(user)

    def add_new_user(self, user):
        """Adds a new user to the db"""

        Db().db_query(f"""
    INSERT INTO users (username, password, created_by)
    VALUES ('{(user[0])}', '{user[1]}', {user[2]});
    """)

    def blacklist_token(self, jti):
        """Blacklists a token"""

        Db().db_query(f"""INSERT INTO blacklist (token) VALUES ('{jti}');""")

    def blacklisted_tokens(self):
        """Blacklists a token"""
        tokenlist = set()
        for tok in Db().get_query('blacklist'):
            token = tok[0]
            tokenlist.add(token)
        return tokenlist

    def promote_demote_user(self, user_id, role):
        """Updates the access level of a user"""

        updatesql = f"""UPDATE users SET role = {role} WHERE id = {user_id};"""
        Db().db_query(updatesql)

    def delete_user(self, user_id):
        """Deletes a user"""
        try:
            Db().db_query(f"""DELETE FROM users WHERE id = {user_id};""")
        except:
            return "Failed", 500
