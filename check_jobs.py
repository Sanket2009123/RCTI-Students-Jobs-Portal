import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
title,
location,
salary
FROM jobs
""")

for row in cursor.fetchall():
    print(row)

conn.close()