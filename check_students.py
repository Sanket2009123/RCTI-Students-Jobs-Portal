import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(resumes)")

rows = cursor.fetchall()

print("\n===== RESUMES TABLE COLUMNS =====")

for row in rows:
    print(
        f"ID={row[0]} | "
        f"NAME={row[1]} | "
        f"TYPE={row[2]}"
    )

conn.close()