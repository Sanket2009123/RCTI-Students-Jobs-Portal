import os
import libsql

url = os.getenv("TURSO_DATABASE_URL")
token = os.getenv("TURSO_AUTH_TOKEN")

if not url or not token:
    raise RuntimeError(
        "TURSO_DATABASE_URL or TURSO_AUTH_TOKEN is missing"
    )

conn = libsql.connect(
    database=url,
    auth_token=token
)

result = conn.execute("SELECT 1").fetchone()

print("Turso connection successful:", result)

conn.close()
