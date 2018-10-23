
c1 = """CREATE TABLE users (
       id SERIAL primary key,
       username VARCHAR(80) UNIQUE not null,
       password VARCHAR(80) not null,
       role INTEGER DEFAULT 1,
       created_by INTEGER,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
"""

c2 = """CREATE TABLE blacklist (
       token VARCHAR
      );
"""

i2 = """
       INSERT INTO users (username, password, role, created_by) VALUES ('owner', 'secret1', 0, 0);
    """


create_tables = [c1, c2, i2]


dr1 = """DROP TABLE IF EXISTS users  CASCADE;"""
dr2 = """DROP TABLE IF EXISTS blacklist  CASCADE;"""

drop_tables = [dr1, dr2]
