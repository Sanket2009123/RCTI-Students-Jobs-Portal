import sqlite3
import os

# ==========================================================
# DATABASE PATH
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "database.db")


# ==========================================================
# COLUMNS TO ADD
# ==========================================================

NEW_COLUMNS = {
    "jobs": {
        "post_date": "TEXT",
        "responsibilities": "TEXT"
    },

    "resumes": {
        "file_name": "TEXT",
        "file_path": "TEXT",
        "file_type": "TEXT",
        "file_size": "INTEGER"
    }
}


# ==========================================================
# UPDATE DATABASE
# ==========================================================

def update_database():

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Database Connected Successfully")

        for table_name, columns in NEW_COLUMNS.items():

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = ?
                """,
                (table_name,)
            )

            if cursor.fetchone() is None:
                print(f"ERROR: '{table_name}' table does not exist.")
                continue

            print(f"\n'{table_name}' table found.")

            cursor.execute(
                f"PRAGMA table_info({table_name})"
            )

            existing_columns = {
                column[1]
                for column in cursor.fetchall()
            }

            for column_name, column_type in columns.items():

                if column_name in existing_columns:
                    print(
                        f"Already exists: "
                        f"{table_name}.{column_name}"
                    )
                    continue

                cursor.execute(
                    f"""
                    ALTER TABLE {table_name}
                    ADD COLUMN {column_name} {column_type}
                    """
                )

                print(
                    f"Added successfully: "
                    f"{table_name}.{column_name}"
                )

        conn.commit()

        print("\n========================================")
        print("DATABASE UPDATED SUCCESSFULLY")
        print("========================================")

    except sqlite3.Error as e:

        if conn:
            conn.rollback()

        print("Database Error:", e)

    except Exception as e:

        if conn:
            conn.rollback()

        print("Error:", e)

    finally:

        if conn:
            conn.close()

        print("\nDatabase connection closed.")


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    update_database()