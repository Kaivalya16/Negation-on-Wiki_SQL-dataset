import sqlite3

conn = sqlite3.connect("data/sqlite_db/test.db")

print("SQLite working successfully!")

conn.close()