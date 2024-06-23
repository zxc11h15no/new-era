import sqlite3
import os

def create_tables():
    # Определяем путь к базе данных
    db_path = os.path.join(os.path.dirname(__file__), '../pharmacy.db')

    # Проверяем существование каталога, если нет, создаем его
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100)
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(100),
        password VARCHAR(100),
        post_id INTEGER,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    );

    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY,
        company_name VARCHAR(255),
        contact_person VARCHAR(255),
        address VARCHAR(255),
        phone_number VARCHAR(15),
        email VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS medicines (
        medicine_id INTEGER PRIMARY KEY,
        medicine_name VARCHAR(255),
        manufacturer VARCHAR(255),
        price INTEGER,
        quantity_in_stock INTEGER
    );

    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        position VARCHAR(100),
        salary INTEGER
    );

    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        address VARCHAR(255),
        phone_number VARCHAR(15),
        email VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        order_status VARCHAR(50),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS order_details (
        detail_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
    );

    CREATE TABLE IF NOT EXISTS employee_orders (
        employee_order_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        order_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );

    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id INTEGER PRIMARY KEY,
        supplier_id INTEGER,
        medicine_id INTEGER,
        delivery_date DATE,
        quantity_delivered INTEGER,
        delivery_cost INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
        FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
    );

    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_id INTEGER,
        amount_paid INTEGER,
        payment_date DATE,
        payment_method VARCHAR(50),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        medicine_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
    );

    CREATE TABLE IF NOT EXISTS reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_name TEXT NOT NULL,
        report_data TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    ''')

    cursor.executescript('''
    INSERT INTO posts (name) VALUES
    ('Администратор'), ('Пользователь'), ('Сотрудник');

    INSERT INTO users (login, password, post_id) VALUES
        ('admin', 'admin', 1), 
        ('user1', 'user', 2), ('user2', 'user', 2), ('user3', 'user', 2), ('user4', 'user', 2), ('user5', 'user', 2),
        ('employee', 'employee', 3);

    INSERT INTO suppliers (supplier_id, company_name, contact_person, address, phone_number, email) VALUES
        (1, 'Фармацевтика АО', 'Иван Иванов', 'ул. Примерная, 1, Город, Страна', '1234567890', 'ivan@example.com'),
        (2, 'Медикал Трейд', 'Мария Смирнова', 'пр. Центральный, 2, Город, Страна', '0987654321', 'maria@example.com'),
        (3, 'Здоровье для всех', 'Алексей Кузнецов', 'пр-т Солнечный, 3, Город, Страна', '1112223333', 'alex@example.com'),
        (4, 'Медснаб', 'Елена Попова', 'ул. Московская, 4, Город, Страна', '5556667777', 'elena@example.com'),
        (5, 'Фармкомплект', 'Дмитрий Иванов', 'пр-т Ленина, 5, Город, Страна', '9998887777', 'dmitry@example.com'),
        (6, 'Аптека РУ', 'Анна Соколова', 'ул. Зеленая, 6, Город, Страна', '4445556666', 'anna@example.com'),
        (7, 'Медсервис', 'Артем Васильев', 'пер. Луговой, 7, Город, Страна', '7778889999', 'artem@example.com'),
        (8, 'Здравник', 'Ольга Новикова', 'ул. Цветочная, 8, Город, Страна', '6665554444', 'olga@example.com'),
        (9, 'Фарма онлайн', 'Владимир Петров', 'пр-т Гагарина, 9, Город, Страна', '2223334444', 'vladimir@example.com'),
        (10, 'Фарммаркет', 'Екатерина Семенова', 'ул. Парковая, 10, Город, Страна', '3334445555', 'ekaterina@example.com');

    INSERT INTO medicines (medicine_id, medicine_name, manufacturer, price, quantity_in_stock) VALUES
        (1, 'Парацетамол', 'ФармаПром', 50, 100),
        (2, 'Ибупрофен', 'МедФарм', 10, 200),
        (3, 'Аспирин', 'ФармКорп', 15, 150),
        (4, 'Цитрамон', 'ЗдравМед', 5, 300),
        (5, 'Нурофен', 'Медика', 80, 50),
        (6, 'Лоратадин', 'АллергФарм', 20, 100),
        (7, 'Амоксициллин', 'АнтибиотикПлюс', 100, 75),
        (8, 'Азитромицин', 'АнтиФарм', 150, 40),
        (9, 'Цефтриаксон', 'Фармакор', 120, 30),
        (10, 'Метформин', 'ДиабетПром', 200, 25);

    INSERT INTO customers (customer_id, first_name, last_name, address, phone_number, email) VALUES
        (1, 'Иван', 'Петров', 'ул. Парковая, 1, Город, Страна', '1112223333', 'ivan@example.com'),
        (2, 'Марина', 'Сидорова', 'пр-т Лесной, 2, Город, Страна', '4445556666', 'marina@example.com'),
        (3, 'Александр', 'Иванов', 'ул. Центральная, 3, Город, Страна', '7778889999', 'alexander@example.com'),
        (4, 'Ольга', 'Кузнецова', 'пр. Солнечный, 4, Город, Страна', '2223334444', 'olga@example.com'),
        (5, 'Виктор', 'Смирнов', 'ул. Гагарина, 5, Город, Страна', '5556667777', 'victor@example.com'),
        (6, 'Татьяна', 'Морозова', 'пер. Луговой, 6, Город, Страна', '8889990000', 'tatiana@example.com'),
        (7, 'Игорь', 'Волков', 'ул. Зеленая, 7, Город, Страна', '3334445555', 'igor@example.com'),
        (8, 'Елена', 'Козлова', 'пр-т Цветочный, 8, Город, Страна', '6667778888', 'elena@example.com'),
        (9, 'Николай', 'Макаров', 'ул. Московская, 9, Город, Страна', '9990001111', 'nikolay@example.com'),
        (10,'Анна', 'Лебедева', 'пр-т Ленина, 10, Город, Страна', '1234567890', 'anna@example.com');

    INSERT INTO orders (order_id, customer_id, order_date, order_status) VALUES
        (1, 1, '2024-03-21', 'В обработке'),
        (2, 2, '2024-03-20', 'Выполнен'),
        (3, 3, '2024-03-19', 'В обработке'),
        (4, 4, '2024-03-18', 'Выполнен'),
        (5, 5, '2024-03-17', 'В обработке'),
        (6, 6, '2024-03-16', 'Выполнен'),
        (7, 7, '2024-03-15', 'В обработке'),
        (8, 8, '2024-03-14', 'Выполнен'),
        (9, 9, '2024-03-13', 'В обработке'),
        (10, 10, '2024-03-12', 'Выполнен');

    INSERT INTO order_details (detail_id, order_id, medicine_id, quantity) VALUES
        (1, 1, 1, 2),
        (2, 1, 2, 1),
        (3, 2, 3, 4),
        (4, 2, 4, 2),
        (5, 3, 5, 1),
        (6, 3, 6, 3),
        (7, 4, 7, 2),
        (8, 4, 8, 1),
        (9, 5, 9, 3),
        (10, 5, 10, 2);

    INSERT INTO payments (payment_id, order_id, customer_id, amount_paid, payment_date, payment_method) VALUES
        (1, 1, 1, 150, '2024-03-21', 'Наличные'),
        (2, 2, 2, 130, '2024-03-20', 'Карта'),
        (3, 3, 3, 115, '2024-03-19', 'Наличные'),
        (4, 4, 4, 220, '2024-03-18', 'Карта'),
        (5, 5, 5, 190, '2024-03-17', 'Наличные'),
        (6, 6, 6, 250, '2024-03-16', 'Карта'),
        (7, 7, 7, 90, '2024-03-15', 'Наличные'),
        (8, 8, 8, 180, '2024-03-14', 'Карта'),
        (9, 9, 9, 120, '2024-03-13', 'Наличные'),
        (10, 10, 10, 200, '2024-03-12', 'Карта');

    INSERT INTO employees (employee_id, first_name, last_name, position, salary) VALUES
        (1, 'Алексей', 'Иванов', 'Менеджер', 50000),
        (2, 'Елена', 'Петрова', 'Ассистент менеджера', 35000),
        (3, 'Иван', 'Смирнов', 'Супервайзер склада', 40000),
        (4, 'Татьяна', 'Кузнецова', 'Кладовщик', 30000),
        (5, 'Андрей', 'Морозов', 'Бухгалтер', 45000),
        (6, 'Елена', 'Новикова', 'Водитель', 32000),
        (7, 'Михаил', 'Васильев', 'Менеджер по обслуживанию клиентов', 35000),
        (8, 'Анастасия', 'Тимофеева', 'Менеджер по продажам', 48000),
        (9, 'Сергей', 'Козлов', 'Агент по закупкам', 42000),
        (10, 'Марина', 'Павлова', 'Маркетолог', 38000);

    INSERT INTO deliveries (delivery_id, supplier_id, medicine_id, delivery_date, quantity_delivered, delivery_cost) VALUES
        (1, 1, 3, '2024-03-21', 50, 1000),
        (2, 2, 1, '2024-03-22', 30, 2000),
        (3, 3, 5, '2024-03-23', 20, 3000),
        (4, 4, 2, '2024-03-24', 40, 4000),
        (5, 5, 4, '2024-03-25', 25, 5000),
        (6, 6, 3, '2024-03-26', 35, 6000),
        (7, 7, 1, '2024-03-27', 45, 7000),
        (8, 8, 5, '2024-03-28', 15, 8000),
        (9, 9, 2, '2024-03-29', 55, 9000),
        (10, 10, 4, '2024-03-30', 10, 10000);

    INSERT INTO employee_orders (employee_order_id, employee_id, order_id) VALUES
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
        (5, 5, 5),
        (6, 6, 6),
        (7, 7, 7),
        (8, 8, 8),
        (9, 9, 9),
        (10, 10, 10);
    ''')

    connection.commit()

    # Проверка данных в таблице users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(f"DEBUG: Users in the database: {users}")

    connection.close()

if __name__ == '__main__':
    create_tables()
