import sqlite3

DB_PATH = "database/database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE resumes
        ADD COLUMN job_title TEXT
    """)

    conn.commit()

    print("✅ job_title column added successfully.")

except sqlite3.OperationalError as e:

    if "duplicate column name" in str(e).lower():
        print("ℹ️ job_title column already exists.")
    else:
        print("❌ Error:", e)

finally:
    conn.close()