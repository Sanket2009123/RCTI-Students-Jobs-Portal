import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE companies
        ADD COLUMN google_id TEXT
    """)

    print("google_id column added successfully.")

except Exception as e:
    print(e)

conn.commit()
conn.close()