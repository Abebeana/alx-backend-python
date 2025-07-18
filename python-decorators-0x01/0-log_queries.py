#!/usr/bin/env python3
"""
0-log_queries.py
Adds a log_queries decorator that prints the SQL statement
together with a timestamp before executing it.
"""

import sqlite3
import functools
from datetime import datetime      

# --------------------------------------------------------------------------- #
# Decorator to log SQL queries with a timestamp
# --------------------------------------------------------------------------- #
def log_queries(func):
    """Print a timestamped log line for every SQL statement executed
    by the wrapped function. Works for positional arg `query`
    or keyword arg `query=...`.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1️ Determine the query string (positional or keyword)
        query = args[0] if args else kwargs.get("query", "")

        # 2 Build a timestamp in ISO format
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3️ Print the log line
        print(f"[{ts}] Executing query: {query}")

        # 4️ Call the original function and return its result
        return func(*args, **kwargs)

    return wrapper

# --------------------------------------------------------------------------- #
# Demo function
# --------------------------------------------------------------------------- #
@log_queries
def fetch_all_users(query):
    """Execute any SELECT/DDL/DML query and return results (if any)."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)

    # Commit only for statements that change data
    if query.strip().lower().startswith(("insert", "update", "delete", "create", "drop", "alter")):
        conn.commit()

    results = cursor.fetchall()  # harmless if no rows
    conn.close()
    return results

# --------------------------------------------------------------------------- #
# Manual test block
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Create simplified users table
    fetch_all_users("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        phone_number TEXT,
        role TEXT NOT NULL CHECK (role IN ('guest', 'host', 'admin')),
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
    """)

    # Insert sample users
    fetch_all_users("""
    INSERT INTO users (first_name, last_name, email, password_hash, phone_number, role)
    VALUES ('Alice', 'Doe', 'alice@example.com', 'hashed_pw_123', '1234567890', 'guest')
    """)

    fetch_all_users("""
    INSERT INTO users (first_name, last_name, email, password_hash, phone_number, role)
    VALUES ('Bob', 'Smith', 'bob@example.com', 'hashed_pw_abc', '0987654321', 'host')
    """)

    # Fetch and print all users
    for row in fetch_all_users("SELECT * FROM users"):
        print(row)
