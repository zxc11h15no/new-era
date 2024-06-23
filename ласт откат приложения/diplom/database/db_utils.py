import sqlite3
import os

def get_db_path():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pharmacy.db'))
    print(f"Используемый путь к базе данных: {db_path}")
    return db_path

def fetch_one(query, params=()):
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            raise Exception(f"База данных не найдена по пути: {db_path}")
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        result = None
    finally:
        connection.close()
    return result

def fetch_all(query, params=()):
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            raise Exception(f"База данных не найдена по пути: {db_path}")
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        result = None
    finally:
        connection.close()
    return result

def execute_query(query, params=()):
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            raise Exception(f"База данных не найдена по пути: {db_path}")
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        connection.close()
