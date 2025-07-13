import sqlite3
import functools

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

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Retrieve a user record by its ID.

    Args:
        conn (sqlite3.Connection): The database connection (injected by decorator).
        user_id (int): The ID of the user to fetch.

    Returns:
        tuple or None: A tuple representing the user's record if found, or None otherwise.
    """
    cursor = conn.cursor()
    
    # Use a parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    
    return cursor.fetchone()

if __name__ == "__main__":
    # Example usage: Fetch user with ID 2
    user = get_user_by_id(1)
    
    if user:
        print("User found:", user)
    else:
        print("User not found.")
