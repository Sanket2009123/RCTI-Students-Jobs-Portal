
import os
import sqlite3
import turso_serverless


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_FILE = os.path.join(BASE_DIR, "database", "schema.sql")


# ==========================================
# ROW COMPATIBILITY
# ==========================================

class HybridRow:

    def __init__(self, values, columns):
        self._values = tuple(values)
        self._data = {
            column[0]: value
            for column, value in zip(columns, self._values)
        }

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._data[key]
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def keys(self):
        return self._data.keys()


# ==========================================
# CURSOR COMPATIBILITY
# ==========================================

class CompatibleCursor:

    def __init__(self, cursor):
        self._cursor = cursor

    @property
    def description(self):
        return self._cursor.description

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def execute(self, sql, params=()):
        self._cursor.execute(sql, params)
        return self

    def executemany(self, sql, params):
        self._cursor.executemany(sql, params)
        return self

    def _convert(self, row):

        if row is None:
            return None

        columns = self._cursor.description or []

        return HybridRow(row, columns)

    def fetchone(self):
        return self._convert(self._cursor.fetchone())

    def fetchall(self):
        return [
            self._convert(row)
            for row in self._cursor.fetchall()
        ]

    def fetchmany(self, size=None):

        if size is None:
            rows = self._cursor.fetchmany()
        else:
            rows = self._cursor.fetchmany(size)

        return [
            self._convert(row)
            for row in rows
        ]

    def close(self):
        self._cursor.close()


# ==========================================
# CONNECTION COMPATIBILITY
# ==========================================

class CompatibleConnection:

    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return CompatibleCursor(
            self._connection.cursor()
        )

    def execute(self, sql, params=()):
        cursor = self.cursor()
        cursor.execute(sql, params)
        return cursor

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()


# ==========================================
# TURSO CLOUD CONNECTION
# ==========================================

def get_connection():

    database_url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")

    if not database_url:
        raise RuntimeError(
            "TURSO_DATABASE_URL is missing."
        )

    if not auth_token:
        raise RuntimeError(
            "TURSO_AUTH_TOKEN is missing."
        )

    if not database_url.startswith("https://"):
        raise RuntimeError(
            "HTTPS Turso database URL required."
        )

    connection = turso_serverless.connect(
        database_url,
        auth_token=auth_token
    )

    return CompatibleConnection(connection)


# ==========================================
# TABLE CHECK
# ==========================================

def table_exists(conn, table_name):

    cursor = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        (table_name,)
    )

    return cursor.fetchone() is not None


# ==========================================
# COLUMN CHECK
# ==========================================

def column_exists(conn, table_name, column_name):

    if not table_exists(conn, table_name):
        return False

    cursor = conn.execute(
        f'PRAGMA table_info("{table_name}")'
    )

    return any(
        row["name"] == column_name
        for row in cursor.fetchall()
    )


# ==========================================
# ADD MISSING COLUMN
# ==========================================

def add_column_if_missing(
    conn,
    table_name,
    column_name,
    column_type
):

    if not table_exists(conn, table_name):
        return

    if not column_exists(conn, table_name, column_name):

        conn.execute(
            f'ALTER TABLE "{table_name}" '
            f'ADD COLUMN "{column_name}" {column_type}'
        )


# ==========================================
# DATABASE MIGRATIONS
# ==========================================

def run_migrations(conn):

    # Students
    add_column_if_missing(
        conn, "students", "google_id", "TEXT"
    )

    # Companies
    add_column_if_missing(
        conn, "companies", "google_id", "TEXT"
    )

    # Jobs
    add_column_if_missing(
        conn, "jobs", "post_date", "TEXT"
    )

    add_column_if_missing(
        conn, "jobs", "responsibilities", "TEXT"
    )

    # Resumes
    add_column_if_missing(
        conn, "resumes", "fullname", "TEXT"
    )

    add_column_if_missing(
        conn, "resumes", "job_title", "TEXT"
    )


# ==========================================
# EXECUTE DATABASE SCHEMA
# ==========================================

def execute_schema(conn):

    if not os.path.exists(SCHEMA_FILE):
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_FILE}"
        )

    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schema = file.read()

    statement = ""

    for line in schema.splitlines():

        statement += line + "\n"

        if sqlite3.complete_statement(statement):

            sql = statement.strip()

            if sql:
                conn.execute(sql)

            statement = ""

    if statement.strip():
        raise RuntimeError(
            "Incomplete SQL statement in schema.sql"
        )


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    conn = get_connection()

    try:

        print("Connecting to Turso Cloud...")

        execute_schema(conn)

        print("Schema checked successfully.")

        run_migrations(conn)

        print("Migrations completed.")

        conn.commit()

        print("Turso database initialized successfully.")

    except Exception as error:

        conn.rollback()

        print("Database error:", error)

        raise

    finally:

        conn.close()
