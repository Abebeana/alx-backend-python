import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""
# Constant for the database file name
DB_NAME = "users.db"

def with_db_connection(func):
    """
    Decorator that automatically opens and closes a database connection.
    
    It injects a sqlite3 connection object as the first argument to the decorated function,
    allowing the wrapped function to operate on the database without managing the connection.
    
    Usage:
        @with_db_connection
        def some_db_function(conn, ...):
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_NAME)  # Open connection to SQLite database
        try:
            return func(conn, *args, **kwargs)  # Call the wrapped function with the connection
        finally:
            conn.close()  # Ensure the connection is closed even if an error occurs
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function call on failure.
    
    Args:
        retries (int): Number of times to retry the function call.
        delay (int): Delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)
            raise Exception("All attempts failed")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        for user in users:
            print(user)
    except Exception as e:
        print(f"Failed to fetch users: {e}")