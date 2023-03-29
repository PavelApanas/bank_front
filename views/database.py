from os.path import join
from sqlite3 import connect

from .settings import BASE_DIR

conn = connect(join(BASE_DIR, 'db.sqlite3'))
cur = conn.cursor()


def create_tables():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS post(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title VARCHAR(128) NOT NULL UNIQUE,
      body TEXT NOT NULL,
      slug VARCHAR(128) NOT NULL UNIQUE,
      author VARCHAR(32) NOT NULL,
      date_created DATETIME DEFAULT now  
    );
    ''')
    conn.commit()


def insert_posts():
    from slugify import slugify
    from datetime import datetime
    posts = [
        (f'Title {i}', f'Body {i}' * 100, slugify(f'Title {i}'), f'author {i}', datetime.now())
        for i in range(20)
    ]


    cur.executemany('''
    INSERT INTO post(title,body,slug,author, date_created)
    values(?, ?, ?, ?, ?);
    ''', posts)

    conn.commit()
