import os
import sys
from dotenv import load_dotenv

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')
# Local imports below
load_dotenv()

name = os.getenv('DEFAULT_OWNER')
password = os.getenv('DEFAULT_OWNER_PASSW')



c1 = """CREATE TABLE users (
       id SERIAL primary key,
       username VARCHAR(80) UNIQUE not null,
       password VARCHAR(80) not null,
       role VARCHAR DEFAULT 'user',
       created_by INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
"""

c2 = """CREATE TABLE books (
       id SERIAL primary key,
       title VARCHAR UNIQUE not null,
       description TEXT,
       category VARCHAR,
       price INTEGER,
       quantity INTEGER,
       minimum INTEGER,
       image_url VARCHAR,
       created_by INTEGER,
       updated_by INTEGER DEFAULT 0,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
"""
c6 = """CREATE TABLE sales (
       id SERIAL primary key,
       book_id INTEGER ARRAY,
       total INTEGER,
       created_by INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       attendant VARCHAR
      );
"""

c4 = """CREATE TABLE categories (
       id INTEGER primary key,
       name VARCHAR
      );
"""

c5 = """CREATE TABLE books_categories (
       id INTEGER primary key,
       category_id INTEGER,
       book_id INTEGER
      );
"""

c3 = """CREATE TABLE blacklist (
       token VARCHAR
      );
"""

i2 = f"""
       INSERT INTO users (username, password, role, created_by) VALUES ('{name}', '{password}', 'admin', 0);
       """

i3 = """ INSERT INTO books (title, description, price, quantity, minimum, image_url, created_by) VALUES ('mpya', '
Lorem ipsum dolor sit amet consectetur, adipisicing elit. Mollitia impedit autem veniam soluta tempora cum repudiandae odit maiores animi, suscipit aspernatur nesciunt architecto nisi pariatur. Maiores beatae impedit similique dignissimos!

', 20, 10, 2, 'https://res.cloudinary.com/danuluma/image/upload/v1541557642/dannstore/aaaindex.png', 0);
    """


create_tables = [c1, c2, c3, c4, c5, c6, i2, i3, i3]


dr1 = """DROP TABLE IF EXISTS users  CASCADE;"""
dr2 = """DROP TABLE IF EXISTS blacklist  CASCADE;"""
dr3 = """DROP TABLE IF EXISTS books  CASCADE;"""
dr4 = """DROP TABLE IF EXISTS categories  CASCADE;"""

dr5 = """DROP TABLE IF EXISTS books_categories CASCADE;"""

dr6 = """DROP TABLE IF EXISTS sales CASCADE;"""

drop_tables = [dr1, dr2, dr3, dr4, dr5, dr6]
