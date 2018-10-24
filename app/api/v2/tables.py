
c1 = """CREATE TABLE users (
       id SERIAL primary key,
       username VARCHAR(80) UNIQUE not null,
       password VARCHAR(80) not null,
       role INTEGER DEFAULT 1,
       created_by INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
"""

c2 = """CREATE TABLE books (
       id SERIAL primary key,
       title VARCHAR UNIQUE not null,
       description VARCHAR,
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
       book_id INTEGER,
       total INTEGER,
       created_by INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

i2 = """
       INSERT INTO users (username, password, role, created_by) VALUES ('owner', 'secret1', 0, 0);
       """

i3 = """ INSERT INTO books (title, description, price, quantity, minimum, image_url, created_by) VALUES ('mpya', 'still testing', 20, 10, 2, 'url', 0);
    """


create_tables = [c1, c2, c3, c4, c5, c6, i2, i3]


dr1 = """DROP TABLE IF EXISTS users  CASCADE;"""
dr2 = """DROP TABLE IF EXISTS blacklist  CASCADE;"""
dr3 = """DROP TABLE IF EXISTS books  CASCADE;"""
dr4 = """DROP TABLE IF EXISTS categories  CASCADE;"""

dr5 = """DROP TABLE IF EXISTS books_categories CASCADE;"""

dr6 = """DROP TABLE IF EXISTS sales CASCADE;"""

drop_tables = [dr1, dr2, dr3, dr4, dr5, dr6]
