import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db



def format_sale(sale):
  """Formats the results to a dictionary"""

  sale = {
            "id": sale[0],
            "details": sale[1],
            "total": sale[2],
            "created_by": sale[3],
            "created_at": sale[4]
      }
  return sale


class SalesModel(Db):
  """Sales Model. Sales Records stuff here"""

  def __init__(self):
    pass

  def get_all_sales(self):
    """Gets all books from the db"""

    records = []
    for sale in Db().get_query('sales'):
      details = format_sale(sale)
      records.append(details)
    return records

  def get_single_book(self, param, this_row):
    """Gets a single sale record"""

    records = [row for row in Db().get_query('sales') if row[this_row] == param]
    if records:
      sale = records[0]
      return format_sale(sale)

  def add_new_(self, book):
    """Adds a new sale record to the db"""
    try:
      Db().db_query(f"""
      INSERT INTO books (details, total, created_by)
      VALUES ('{book[0]}', {book[1]}, {book[2]});
      """)
    except:
      return "Failed to add", 500

