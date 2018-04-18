import pymssql

import pdb
stop = pdb.set_trace

server   = "aungram.database.windows.net"
database = "aungram"
username = "auni@aungram"
password = "L!nguistics"

class Database:
  def __init__(self):
    self.conn = pymssql.connect(server, username, password, database)
    self.cursor = self.conn.cursor()

  def execute(self, query):
    self.cursor.execute(query)
    return self.cursor

  def execute(self, query, *params):
    self.cursor.execute(query, params)
    return self.cursor

  def insert(self, value):
    query = '''
      UPDATE bigrams
        set count=%d
      WHERE w1=%s and w2=%s and year=%d
      IF @@ROWCOUNT = 0
        INSERT INTO bigrams
        VALUES (%s, %s, %d, %d)
      '''
    self.cursor.execute(query, value)

  def insertmany(self, values):
    self.cursor.executemany('''
      UPDATE bigrams
        set count=%d
      WHERE w1=%s and w2=%s and year=%d
      IF @@ROWCOUNT = 0
        INSERT INTO bigrams
        VALUES (%s, %s, %d, %d)
      ''',
      values
    )

  def executemany(self, query, values):
    self.cursor.executemany(query, values)

  def reset_table(self):
    self.execute('''
    IF OBJECT_ID('bigrams', 'U') IS NOT NULL
      DROP TABLE bigrams
    CREATE TABLE bigrams (
      w1 VARCHAR(100) NOT NULL,
      w2 VARCHAR(100) NOT NULL,
      year INT NOT NULL,
      count INT NOT NULL,
      PRIMARY KEY(w1, w2, year)
    )
    ''')

  def read(self, query):
    self.cursor.execute(query)
    return self.cursor

  def close(self):
    self.conn.commit()
    self.conn.close()

if __name__ == "__main__":
  db = Database()
  print len(list(db.read("SELECT * FROM bigrams")))
  db.close()
