# coding: utf-8

# create tables in an empty SQLite database for later use

import sqlite3

DB_SETUP = '''

CREATE TABLE IF NOT EXISTS users (
  user VARCHAR(10),
  is_admin BOOLEAN,
  password VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS places (
  valregexp VARCHAR(99),
  place VARCHAR(20),
  max_length INTEGER,
  min_length INTEGER,
  user VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS numbers (
  time TIMESTAMP NOT NULL,
  number VARCHAR(30) NOT NULL,
  user VARCHAR(10),
  place VARCHAR(20) NOT NULL,
  fingerprint VARCHAR(32) NOT NULL
);

CREATE UNIQUE INDEX i1 ON numbers(number, fingerprint);
--- CREATE UNIQUE INDEX numbers_unique ON numbers(number, fingerprint, place);

'''


def create_tables(connection):
    """
    Intializes all necessary tables, run only first time
    :param connection:
    :return:
    """

    with connection:

        cursor = connection.cursor()
        # create all tables
        cursor.executescript(DB_SETUP)

        # write initial record for location and user
        initial_queries = (
            (
                'INSERT INTO places(place, user, valregexp, min_length, max_length) VALUES (?,?,?,?,?)',
                ("LAGESO", "Helper", "^[a-zA-Z]{1,1}[0-9]+$", 1, 99)
            ),
            (
                'INSERT INTO users(user, password, is_admin) VALUES (?,?,?)',
                ("Helper", "1234", "-")
            ),
            (
                'INSERT INTO numbers(number, time, place, user, fingerprint) VALUES (?,?,?,?,?)',
                ("A00000", "Nov 14 2011 03:12:12:947PM", "-", "-", "-")
            ),
        )

        for query, values in initial_queries:
            try:
                cursor.execute(query, values)
            except sqlite3.OperationalError as e:
                print('[ERROR]:   \t{}\n           {}'.format(e, query_string))
                raise


def initialize_database(path):
    db = sqlite3.connect(path)
    create_tables(db)

    cur = db.cursor()

    cur.execute('SELECT name FROM sqlite_master WHERE type=?', ("table",))

    for row in cur.fetchall():
        print(row)

    db.close()


if __name__ == '__main__':

    initialize_database('lagesonr.db')
