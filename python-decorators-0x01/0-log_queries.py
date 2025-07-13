import sqlite3
import functools

# Decorator to log SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', '')
        print(f"Executing query: {query}")
        return func(*args, **kwargs)    
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results



if __name__ == "__main__":
    #### fetch users while logging the query
    users = fetch_all_users(query="create table if not exists users (id INTEGER PRIMARY KEY, name TEXT)")
    users = fetch_all_users(query="INSERT INTO users (name) VALUES ('Alice')")
    users = fetch_all_users(query="INSERT INTO users (name) VALUES ('Bob')")

    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)