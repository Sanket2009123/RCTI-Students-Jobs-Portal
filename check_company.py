import sqlite3

conn = sqlite3.connect("database/database.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(companies)")

for row in cursor.fetchall():
    print(dict(row))

conn.close()