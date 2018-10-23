import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db



def format_book(book):
  """Formats the results to a dictionary"""

  book = {
            "id": book[0],
            "title": book[1],
            "description": book[2],
            "category": book[3],
            "price": book[4],
            "quantity": book[5],
            "minimum": book[6],
            "image_url": book[7],
            "created_by": book[8],
            "created_at": str(book[9])
      }
  return book


class ProductModel(Db):
  """Product Model. Books stuff here"""

  def __init__(self):
    pass

  def get_all_books(self):
    """Gets all books from the db"""

    booklist = []
    for book in Db().get_query('books'):
      details = format_book(book)
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
    try:
      Db().db_query(f"""
      INSERT INTO books (title, description, category, price, quantity, minimum, image_url, created_by)
      VALUES ('{book[0]}', '{book[1]}', {book[2]}, {book[3]}, {book[4]}, '{book[5]}', {book[6]});
      """)
    except:
      return "Failed to add"

  def edit_book(self, user_id, book):
    """Updates a book's details"""
    title = book[0]
    description = book[1]
    price = book[2]
    quantity = book[3]
    minimum = book[4]
    image_url = book[5]
    my_id = book[6]

    details = {
        "title": '"' + 'book3' + '"',
        "description": '"' + "Lorem ipsum" + '"',
        "description": '"' + "Fiction" + '"',
        "price": 110,
        "quantity": 50,
        "minimum": 4,
        "image_url": '"' + "new_url" + '"',
        "created_by": 0,
        "updated_by":0
        }
    for key,value in details.items():
        updatesql = f"""UPDATE users SET {key} = {value} WHERE id = {user_id};"""
        Db().db_query(updatesql)


  def delete_book(self, book_id):
    """Deletes a book"""

    Db().db_query(f"""DELETE FROM books WHERE id = {book_id};""")
