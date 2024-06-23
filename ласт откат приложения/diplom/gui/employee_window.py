from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, \
    QLineEdit, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from utils.db_utils import execute_query, fetch_all

class EmployeeWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Сотрудник - Парацетамол')
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

        self.label_title = QLabel('Онлайн аптека')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.button_manage_medicines = self.create_button('Управление товарами')
        self.button_manage_medicines.clicked.connect(self.manage_medicines)
        layout.addWidget(self.button_manage_medicines)

        self.button_view_order_quantity = self.create_button('Просмотр количества заказов')
        self.button_view_order_quantity.clicked.connect(self.view_order_quantity)
        layout.addWidget(self.button_view_order_quantity)

        self.button_view_order_info = self.create_button('Просмотр информации заказов')
        self.button_view_order_info.clicked.connect(self.view_order_info)
        layout.addWidget(self.button_view_order_info)

        self.button_view_medicines_quantity = self.create_button('Просмотр количества товаров')
        self.button_view_medicines_quantity.clicked.connect(self.view_medicines_quantity)
        layout.addWidget(self.button_view_medicines_quantity)

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

    def manage_medicines(self):
        self.medicines_window = ManageMedicinesWindow()
        self.medicines_window.show()

    def view_order_quantity(self):
        orders = fetch_all("SELECT COUNT(*) FROM orders")
        QMessageBox.information(self, 'Количество заказов', f"Количество заказов: {orders[0][0]}")

    def view_order_info(self):
        orders = fetch_all("SELECT * FROM orders")
        self.order_info_window = OrderInfoWindow(orders)
        self.order_info_window.show()

    def view_medicines_quantity(self):
        medicines_quantity = fetch_all("SELECT medicine_name, quantity_in_stock FROM medicines")
        self.medicines_quantity_window = MedicinesQuantityWindow(medicines_quantity)
        self.medicines_quantity_window.show()

    def back(self):
        self.close()

class ManageMedicinesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление товарами - Парацетамол')
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

        self.label_title = QLabel('Управление товарами')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить товар')
        self.button_add.clicked.connect(self.add_medicine)
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить товар')
        self.button_delete.clicked.connect(self.delete_medicine)
        layout.addWidget(self.button_delete)

        self.button_update = self.create_button('Изменить товар')
        self.button_update.clicked.connect(self.update_medicine)
        layout.addWidget(self.button_update)

        self.button_load = self.create_button('Загрузить товары')
        self.button_load.clicked.connect(self.load_medicines)
        layout.addWidget(self.button_load)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_medicines()

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

    def load_medicines(self):
        medicines = fetch_all("SELECT * FROM medicines")
        self.table.setRowCount(len(medicines))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Производитель', 'Цена', 'Количество на складе'])

        for row_index, row_data in enumerate(medicines):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_medicine(self):
        try:
            medicine_name, ok = QInputDialog.getText(self, 'Название товара', 'Введите название:')
            if not ok or not medicine_name:
                return
            manufacturer, ok = QInputDialog.getText(self, 'Производитель', 'Введите производителя:')
            if not ok or not manufacturer:
                return
            price, ok = QInputDialog.getInt(self, 'Цена', 'Введите цену:')
            if not ok or not price:
                return
            quantity_in_stock, ok = QInputDialog.getInt(self, 'Количество на складе', 'Введите количество на складе:')
            if not ok or not quantity_in_stock:
                return

            execute_query(
                "INSERT INTO medicines (medicine_name, manufacturer, price, quantity_in_stock) VALUES (?, ?, ?, ?)",
                (medicine_name, manufacturer, price, quantity_in_stock))
            QMessageBox.information(self, 'Успех', 'Товар добавлен')
            self.load_medicines()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка добавления товара: {str(e)}')

    def delete_medicine(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления')
            return

        try:
            medicine_id = self.table.item(row, 0).text()
            execute_query("DELETE FROM medicines WHERE medicine_id = ?", (medicine_id,))
            QMessageBox.information(self, 'Успех', 'Товар удален')
            self.load_medicines()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления товара: {str(e)}')

    def update_medicine(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для изменения')
            return

        try:
            medicine_id = self.table.item(row, 0).text()
            medicine_name, ok = QInputDialog.getText(self, 'Название товара', 'Введите название:',
                                                     text=self.table.item(row, 1).text())
            if not ok or not medicine_name:
                return
            manufacturer, ok = QInputDialog.getText(self, 'Производитель', 'Введите производителя:',
                                                    text=self.table.item(row, 2).text())
            if not ok or not manufacturer:
                return
            price, ok = QInputDialog.getInt(self, 'Цена', 'Введите цену:', value=int(self.table.item(row, 3).text()))
            if not ok or not price:
                return
            quantity_in_stock, ok = QInputDialog.getInt(self, 'Количество на складе', 'Введите количество на складе:',
                                                        value=int(self.table.item(row, 4).text()))
            if not ok or not quantity_in_stock:
                return

            execute_query(
                "UPDATE medicines SET medicine_name = ?, manufacturer = ?, price = ?, quantity_in_stock = ? WHERE medicine_id = ?",
                (medicine_name, manufacturer, price, quantity_in_stock, medicine_id))
            QMessageBox.information(self, 'Успех', 'Товар изменен')
            self.load_medicines()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка изменения товара: {str(e)}')

    def back(self):
        self.close()

class OrderInfoWindow(QMainWindow):
    def __init__(self, orders):
        super().__init__()
        self.setWindowTitle('Информация о заказах - Парацетамол')
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
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Customer ID', 'Order Date', 'Status', 'Total Price'])
        self.table.setRowCount(len(orders))

        for row_index, row_data in enumerate(orders):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

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

    def back(self):
        self.close()

class MedicinesQuantityWindow(QMainWindow):
    def __init__(self, medicines_quantity):
        super().__init__()
        self.setWindowTitle('Количество товаров - Парацетамол')
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

        self.label_title = QLabel('Количество товаров на складе')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название', 'Количество'])
        self.table.setRowCount(len(medicines_quantity))

        for row_index, row_data in enumerate(medicines_quantity):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        layout.addWidget(self.table)

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

    def back(self):
        self.close()
