import sqlite3
import os

def get_db_path():
    return os.path.join(os.path.dirname(__file__), '../pharmacy.db')

def test_db():
    db_path = get_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Проверяем наличие таблицы users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()

    if table_exists:
        print("Таблица 'users' существует.")
    else:
        print("Таблица 'users' НЕ существует.")

    # Выводим все таблицы для проверки
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Все таблицы в базе данных:", tables)

    connection.close()

if __name__ == '__main__':
    test_db()
