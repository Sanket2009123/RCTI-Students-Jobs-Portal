import sqlite3
import os

DB_PATH = "database/database.db"

print("Database path:")
print(os.path.abspath(DB_PATH))

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT id, company_name, email, status FROM companies")

companies = cursor.fetchall()

print("\nCompanies found:", len(companies))

for company in companies:
    print(
        company["id"],
        "|",
        company["company_name"],
        "|",
        company["email"],
        "|",
        company["status"]
    )

conn.close()