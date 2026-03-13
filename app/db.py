import sqlite3

DB_PATH = "sandbox.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS executions (
            execution_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            code TEXT NOT NULL,
            stdout TEXT,
            stderr TEXT,
            exit_code INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id)
        )
    """)

    conn.commit()
    conn.close()

def save_session(session_id, user_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sessions (session_id, user_id, title) VALUES (?, ?, ?)",
        (session_id, user_id, title)
    )

    conn.commit()
    conn.close()


def save_execution(execution_id, session_id, code, stdout, stderr, exit_code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO executions (execution_id, session_id, code, stdout, stderr, exit_code) VALUES (?, ?, ?, ?, ?, ?)",
        (execution_id, session_id, code, stdout, stderr, exit_code)
    )

    conn.commit()
    conn.close()