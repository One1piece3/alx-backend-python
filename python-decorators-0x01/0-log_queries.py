#!/usr/bin/env python3
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # On suppose que la requête SQL est passée soit comme argument positionnel soit nommé "query"
        query = None
        if "query" in kwargs:
            query = kwargs["query"]
        elif len(args) > 0:
            query = args[0]

        if query:
            print(f"[LOG] Executing SQL Query: {query}")

        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Exemple : récupération et affichage des utilisateurs
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)

