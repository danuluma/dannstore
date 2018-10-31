import os
import sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


def format_sale(sale):
    """Formats the results to a dictionary"""

    sale = {
        "id": sale[0],
        "book_id": sale[1],
        "total": sale[2],
        "created_by": sale[3],
        "created_at": str(sale[4])
    }
    return sale


class SalesModel(Db):
    """Sales Model. Sales Records stuff here"""

    def get_all_sales(self):
        """Gets all sales records from the db"""

        records = []
        for sale in Db().get_query('sales'):
            details = format_sale(sale)
            records.append(details)
        return records

    def get_single_sale(self, param, this_col):
        """Gets a single sale record"""

        records = [row for row in Db().get_query(
            'sales') if row[this_col] == param]
        if records:
            sale = records[0]
            return format_sale(sale)

    def add_new_record(self, new_sale):
        """Adds a new sale record to the db"""

        try:
            Db().db_query(f"""
      INSERT INTO sales (book_id, total, created_by)
      VALUES ('{new_sale[0]}', {new_sale[1]}, {new_sale[2]});
      """)
        except:
            return "Failed to add", 500
