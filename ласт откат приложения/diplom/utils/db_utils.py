import sqlite3

def fetch_one(query, params=()):
    connection = sqlite3.connect('../pharmacy.db')
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    connection.close()
    return result

def fetch_all(query, params=()):
    connection = sqlite3.connect('../pharmacy.db')
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    connection.close()
    return result

def execute_query(query, params=()):
    connection = sqlite3.connect('../pharmacy.db')
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()
