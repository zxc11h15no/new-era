from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QInputDialog, QHBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QPalette, QPixmap, QBrush
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all, fetch_one

class UserWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Пользователь - Парацетамол')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QGridLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name, 0, 0, 1, 2)

        self.button_view_medicines = self.create_button('Каталог')
        self.button_view_medicines.clicked.connect(self.view_medicines)
        layout.addWidget(self.button_view_medicines, 1, 0)

        self.button_view_cart = self.create_button('Корзина')
        self.button_view_cart.clicked.connect(self.view_cart)
        layout.addWidget(self.button_view_cart, 1, 1)

        self.button_view_orders = self.create_button('Заказы')
        self.button_view_orders.clicked.connect(self.view_orders)
        layout.addWidget(self.button_view_orders, 2, 0)

        self.button_profile = self.create_button('Профиль')
        self.button_profile.clicked.connect(self.open_profile)
        layout.addWidget(self.button_profile, 2, 1)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back, 3, 0, 1, 2)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def view_medicines(self):
        try:
            print("DEBUG: Fetching medicines...")  # Отладочная информация
            medicines = fetch_all("SELECT * FROM medicines")
            print(f"DEBUG: Fetched medicines: {medicines}")  # Отладочная информация
            self.medicines_window = MedicinesWindow(medicines, self.user_id)
            self.medicines_window.show()
            print("DEBUG: MedicinesWindow shown")  # Отладочная информация
        except Exception as e:
            print(f"DEBUG: Error fetching medicines: {e}")  # Отладочная информация
            QMessageBox.critical(self, 'Ошибка', f'Ошибка получения данных о товарах: {str(e)}')

    def view_cart(self):
        self.cart_window = CartWindow(self.user_id)
        self.cart_window.show()

    def view_orders(self):
        try:
            orders = fetch_all("SELECT * FROM orders WHERE customer_id = ?", (self.user_id,))
            self.orders_window = OrdersWindow(orders)
            self.orders_window.show()
        except Exception as e:
            print(f"DEBUG: Error fetching orders: {e}")  # Отладочная информация
            QMessageBox.critical(self, 'Ошибка', f'Ошибка получения данных о заказах: {str(e)}')

    def open_profile(self):
        self.profile_window = ProfileWindow(self.user_id)
        self.profile_window.show()

    def back(self):
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class MedicinesWindow(QMainWindow):
    def __init__(self, medicines, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Просмотр товаров - Парацетамол')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_title = QLabel('Товары')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Цена', 'Количество на складе', ''])
        self.table.setRowCount(len(medicines))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("background: transparent;")

        for row_index, row_data in enumerate(medicines):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            add_button = QPushButton('Добавить в корзину')
            add_button.clicked.connect(lambda _, r=row_index: self.add_to_cart(r))
            self.table.setCellWidget(row_index, 5, add_button)

        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()

        self.button_view_cart = self.create_button('Перейти в корзину')
        self.button_view_cart.clicked.connect(self.view_cart)
        buttons_layout.addWidget(self.button_view_cart)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        buttons_layout.addWidget(self.button_back)

        layout.addLayout(buttons_layout)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def add_to_cart(self, row):
        medicine_id = self.table.item(row, 0).text()
        medicine_name = self.table.item(row, 1).text()
        stock_quantity = int(self.table.item(row, 4).text())
        quantity, ok = QInputDialog.getInt(self, 'Количество', f'Введите количество для "{medicine_name}":', 1, 1, stock_quantity)
        if not ok or not quantity:
            return

        try:
            execute_query("INSERT INTO cart (user_id, medicine_id, quantity) VALUES (?, ?, ?)", (self.user_id, medicine_id, quantity))
            QMessageBox.information(self, 'Успех', 'Товар добавлен в корзину')
        except Exception as e:
            print(f"DEBUG: Error adding to cart: {e}")  # Отладочная информация
            QMessageBox.critical(self, 'Ошибка', f'Ошибка добавления товара в корзину: {str(e)}')

    def view_cart(self):
        self.cart_window = CartWindow(self.user_id)
        self.cart_window.show()

    def back(self):
        self.close()

class CartWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Корзина - Парацетамол')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_title = QLabel('Корзина')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Количество', 'Цена'])
        layout.addWidget(self.table)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("background: transparent;")

        self.label_total = QLabel('Общая сумма: 0')
        self.label_total.setFont(QFont('Arial', 14))
        self.label_total.setStyleSheet("color: brown;")
        layout.addWidget(self.label_total)

        self.button_remove_from_cart = self.create_button('Удалить из корзины')
        self.button_remove_from_cart.clicked.connect(self.remove_from_cart)
        layout.addWidget(self.button_remove_from_cart)

        self.button_create_order = self.create_button('Сделать заказ')
        self.button_create_order.clicked.connect(self.create_order)
        layout.addWidget(self.button_create_order)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_cart()

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def load_cart(self):
        cart_items = fetch_all("""
            SELECT cart.id, medicines.medicine_name, cart.quantity, medicines.price 
            FROM cart 
            JOIN medicines ON cart.medicine_id = medicines.medicine_id
            WHERE cart.user_id = ?
        """, (self.user_id,))
        self.table.setRowCount(len(cart_items))

        total = 0
        for row_index, row_data in enumerate(cart_items):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
                if col_index == 3:
                    total += row_data[2] * row_data[3]

        self.label_total.setText(f'Общая сумма: {total}')

    def remove_from_cart(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления из корзины')
            return

        cart_id = self.table.item(row, 0).text()
        execute_query("DELETE FROM cart WHERE id = ?", (cart_id,))
        QMessageBox.information(self, 'Успех', 'Товар удален из корзины')
        self.load_cart()

    def create_order(self):
        cart_items = fetch_all("SELECT medicine_id, quantity FROM cart WHERE user_id = ?", (self.user_id,))
        if not cart_items:
            QMessageBox.warning(self, 'Ошибка', 'Корзина пуста')
            return

        execute_query(
            "INSERT INTO orders (customer_id, order_date, order_status) VALUES (?, date('now'), 'В обработке')",
            (self.user_id,))
        order_id = fetch_one("SELECT last_insert_rowid()")[0]

        for medicine_id, quantity in cart_items:
            execute_query("INSERT INTO order_details (order_id, medicine_id, quantity) VALUES (?, ?, ?)",
                          (order_id, medicine_id, quantity))

        execute_query("DELETE FROM cart WHERE user_id = ?", (self.user_id,))
        QMessageBox.information(self, 'Успех', 'Заказ создан')
        self.close()

    def back(self):
        self.close()

class OrdersWindow(QMainWindow):
    def __init__(self, orders):
        super().__init__()
        self.setWindowTitle('Просмотр заказов - Парацетамол')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_title = QLabel('Заказы')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: brown;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Customer ID', 'Order Date', 'Status'])
        self.table.setRowCount(len(orders))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("background: transparent;")

        for row_index, row_data in enumerate(orders):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

        self.button_back = QPushButton('Назад')
        self.button_back.setFont(QFont('Arial', 14))
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def back(self):
        self.close()

class ProfileWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Профиль - Парацетамол')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.button_change_credentials = self.create_button('Смена логина или пароля')
        self.button_change_credentials.clicked.connect(self.change_credentials)
        layout.addWidget(self.button_change_credentials)

        self.button_change_personal_info = self.create_button('Смена личных данных')
        self.button_change_personal_info.clicked.connect(self.change_personal_info)
        layout.addWidget(self.button_change_personal_info)

        self.button_view_orders = self.create_button('Заказы')
        self.button_view_orders.clicked.connect(self.view_orders)
        layout.addWidget(self.button_view_orders)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        return button

    def change_credentials(self):
        self.update_user_window = UpdateUserWindow(self.user_id)
        self.update_user_window.show()

    def change_personal_info(self):
        self.update_personal_info_window = UpdatePersonalInfoWindow(self.user_id)
        self.update_personal_info_window.show()

    def view_orders(self):
        orders = fetch_all("SELECT * FROM orders WHERE customer_id = ?", (self.user_id,))
        self.orders_window = OrdersWindow(orders)
        self.orders_window.show()

    def back(self):
        self.close()

class UpdateUserWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Смена логина или пароля - Парацетамол')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_login = QLabel('Новый логин:')
        layout.addWidget(self.label_login)

        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        self.label_password = QLabel('Новый пароль:')
        layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        layout.addWidget(self.input_password)

        self.button_update = QPushButton('Обновить')
        self.button_update.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_update.clicked.connect(self.update_user_in_db)
        layout.addWidget(self.button_update)

        self.button_back = QPushButton('Назад')
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def update_user_in_db(self):
        login = self.input_login.text()
        password = self.input_password.text()

        try:
            execute_query("UPDATE users SET login=?, password=? WHERE id=?", (login, password, self.user_id))
            QMessageBox.information(self, 'Успех', 'Данные пользователя обновлены')
            self.close()
        except Exception as e:
            print(f"DEBUG: Error updating user: {e}")  # Отладочная информация
            QMessageBox.critical(self, 'Ошибка', f'Ошибка обновления данных пользователя: {str(e)}')

    def back(self):
        self.close()

class UpdatePersonalInfoWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('Смена личных данных - Парацетамол')
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Arial', 24))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_first_name = QLabel('Имя:')
        layout.addWidget(self.label_first_name)
        self.input_first_name = QLineEdit()
        layout.addWidget(self.input_first_name)

        self.label_last_name = QLabel('Фамилия:')
        layout.addWidget(self.label_last_name)
        self.input_last_name = QLineEdit()
        layout.addWidget(self.input_last_name)

        self.label_address = QLabel('Адрес:')
        layout.addWidget(self.label_address)
        self.input_address = QLineEdit()
        layout.addWidget(self.input_address)

        self.label_phone = QLabel('Телефон:')
        layout.addWidget(self.label_phone)
        self.input_phone = QLineEdit()
        layout.addWidget(self.input_phone)

        self.label_email = QLabel('Email:')
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)

        self.button_update = QPushButton('Обновить')
        self.button_update.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_update.clicked.connect(self.update_personal_info_in_db)
        layout.addWidget(self.button_update)

        self.button_back = QPushButton('Назад')
        self.button_back.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_user_data()

    def set_background(self):
        palette = QPalette()
        pixmap = QPixmap("img/pharmacy_background.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def load_user_data(self):
        user_data = fetch_one("SELECT first_name, last_name, address, phone_number, email FROM customers WHERE customer_id = ?", (self.user_id,))
        if user_data:
            self.input_first_name.setText(user_data[0])
            self.input_last_name.setText(user_data[1])
            self.input_address.setText(user_data[2])
            self.input_phone.setText(user_data[3])
            self.input_email.setText(user_data[4])

    def update_personal_info_in_db(self):
        first_name = self.input_first_name.text()
        last_name = self.input_last_name.text()
        address = self.input_address.text()
        phone = self.input_phone.text()
        email = self.input_email.text()

        try:
            execute_query("UPDATE customers SET first_name=?, last_name=?, address=?, phone_number=?, email=? WHERE customer_id=?",
                          (first_name, last_name, address, phone, email, self.user_id))
            QMessageBox.information(self, 'Успех', 'Личные данные обновлены')
            self.close()
        except Exception as e:
            print(f"DEBUG: Error updating personal info: {e}")  # Отладочная информация
            QMessageBox.critical(self, 'Ошибка', f'Ошибка обновления личных данных: {str(e)}')

    def back(self):
        self.close()
