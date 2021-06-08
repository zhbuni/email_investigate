from SQLiteClass import DB

db = DB("database.db")
db.drop_db()
db.create_db()
db.fill_db()
