from db import Database

if __name__ == '__main__':
  db = Database()
  db.reset_table()
  db.close()
