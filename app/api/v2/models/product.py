import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db



def format_book(user):
  """Formats the results to a dictionary"""

  book = {
            "id": user[0],
            "title": user[1],
            "description": user[2],
            "price": user[3],
            "quantity": user[4],
            "minimum": user[5],
            "image_url": user[6],
            "created_by": user[7],
            "created_at": str(user[8])
      }
  return book


class ProductModel(Db):
  """Product Model. Books stuff here"""

  def __init__(self):
    pass

  def get_all_books(self):
    """Gets all books from the db"""

    booklist = []
    for user in Db().get_query('books'):
      details = format_book(user)
      booklist.append(details)
    return booklist

  def get_single_book(self, param, this_row):
    """Gets a single book"""

    books = [row for row in Db().get_query('books') if row[this_row] == param]
    if books:
      book = books[0]
      return format_book(book)

  def add_new_book(self, book):
    """Adds a new book to the db"""

    Db().db_query(f"""
    INSERT INTO books (title, description, price, quantity, minimum, image_url, created_by)
    VALUES ('{book[0]}', '{book[1]}', {book[2]}, {book[3]}, {book[4]}, '{book[5]}', {book[6]});
    """)

  def delete_book(self, book_id):
    """Deletes a book"""

    Db().db_query(f"""DELETE FROM books WHERE id = {book_id};""")
