from database.db import get_connection

try:
    conn = get_connection()

    result = conn.execute("SELECT 1").fetchone()

    print("Turso Connected Successfully!")
    print(result)

    conn.close()

except Exception as e:
    print("Connection Failed:", e)
