import sqlite3

print("Program Started")

try:
    conn = sqlite3.connect("database/database.db")
    print("Database Connected")

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(jobs)")
    rows = cursor.fetchall()

    print("Total Columns:", len(rows))

    for row in rows:
        print(row)

    conn.close()
    print("Done")

except Exception as e:
    print("Error:", e)