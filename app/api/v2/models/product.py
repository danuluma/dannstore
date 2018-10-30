import os
import sys

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
        "updated_by": book[9],
        "created_at": str(book[10])
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

        books = [row for row in Db().get_query(
            'books') if row[this_row] == param]
        if books:
            book = books[0]
            return format_book(book)

    def add_new_book(self, book):
        """Adds a new book to the db"""
        try:
            Db().db_query(f"""
      INSERT INTO books (title, description, category, price, quantity, minimum, image_url, created_by)
      VALUES ('{book[0]}', '{book[1]}', '{book[2]}', {book[3]}, {book[4]}, {book[5]}, '{book[6]}', {book[7]});
      """)
        except:
            return "Failed to add", 500

    def edit_book(self, book_id, book):
        """Updates a book's details"""

        Db().db_query(f"""UPDATE books SET title = '{book[0]}', description = '{book[1]}',  category = '{book[2]}', price = {book[3]}, quantity = {book[4]}, minimum = {book[5]}, image_url = '{book[6]}', updated_by = {book[7]} WHERE id = {book_id};""")

    def delete_book(self, book_id):
        """Deletes a book"""
        try:
            Db().db_query(f"""DELETE FROM books WHERE id = {book_id};""")
        except:
            return "Failed", 500

