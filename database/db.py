import os
import turso_serverless

def get_connection():

    url = os.getenv("TURSO_DATABASE_URL")
    token = os.getenv("TURSO_AUTH_TOKEN")

    if not url or not token:
        raise ValueError("Turso credentials missing")

    if not url.startswith("https://"):
        raise ValueError("HTTPS Turso database URL required")

    conn = turso_serverless.connect(
        url,
        auth_token=token
    )

    return conn
