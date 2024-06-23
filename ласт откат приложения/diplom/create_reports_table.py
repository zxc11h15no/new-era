import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()

# Создание таблицы reports, если её нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

# Добавление тестовых данных в таблицу reports
cursor.execute("INSERT INTO reports (name, date) VALUES (?, ?)", ('Отчет 1', '2023-06-01'))
cursor.execute("INSERT INTO reports (name, date) VALUES (?, ?)", ('Отчет 2', '2023-06-02'))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Table 'reports' created and test data added successfully.")
