from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys
from flask import Flask

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
# Local imports below
from app.api.v2.tables import create_tables, drop_tables
from config import app_config


load_dotenv()


class Db(object):
  """Database stuff"""

  def __init__(self):
    self.dbase = app_config[os.getenv('APP_SETTINGS')].DB_URI

  def connect(self):
    """Creates a connection and returns it."""

    try:
      """Try creating a connection to an existing database"""

      conn = psycopg2.connect(self.dbase)
      print("Connection successful")
      return conn
    except:
      print("Error connecting......Hold on while I create one")
      try:
        """Try creating the databases and return a connection"""

        conn = psycopg2.connect(os.getenv("HOST"))
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        try:
          cur.execute("""CREATE DATABASE {};""".format(os.getenv("DEV_DBNAME")))
          print("Congrats!! Danns dev database created")
        except:
          pass
        try:
          cur.execute("""CREATE DATABASE {};""".format(os.getenv("TEST_DBNAME")))
          print("Congrats!! Danns test database created")
        except:
          pass
        conn.commit()
        cur.close()
        return psycopg2.connect(self.dbase)
      except:
        """Sijui nitaambia nini watu.."""

        return("Sorry couldn't")


  def run_query(self, queries):
    """Run sql queries supplied. expects a list or any enumerable"""

    for query in queries:
      try:
          conn = Db().connect()
          cur = conn.cursor()
          cur.execute(query)
          conn.commit()
          cur.close()
          conn.close()
      except:
        pass

  def create(self):
    """Creates the necessary tables"""

    Db().run_query(create_tables)

  def drop(self):
    """Drop tables when needed"""

    Db().run_query(drop_tables)

  def get_query(self, table):
    """Perfoms SELECT queries"""

    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM {table}""")
    return [row for row in cur.fetchall()]

  def db_query(self, db_query):
    """POST, PUT and DELETE queries handled here"""

    conn = Db().connect()
    cur = conn.cursor()
    cur.execute(db_query)
    conn.commit()
    conn.close()

