import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""
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
def cache_query(func):
    """Decorator to cache the results of a query.
    It stores the results in a dictionary using the query string as the key.
    """
    

    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("Returning cached result")
            return query_cache[query]
        result = func(conn, query)
        query_cache[query] = result
        return result

    return wrapper




@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # Example usage: Fetch users with caching
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    for user in users:
        print(f"user: {user}")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    for user in users_again:
        print(f"user again: {user}")
