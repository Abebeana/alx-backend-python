import sqlite3 
import functools



DB_NAME = "users.db"

"""your code goes here"""
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
def transactional(func):
    """Decorator to handle transactions automatically.
    It commits the transaction if the function executes successfully,
    or rolls it back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Call the wrapped function
            conn.commit()  # Commit the transaction
            return result
        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            print(f"Transaction failed: {e}")
            raise  # Re-raise the exception for further handling
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE user_id = ?", (new_email, user_id))
    ### Update user's email with automatic transaction handling

if __name__ == "__main__": 
    # Example usage: Update user with ID 1's email
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')