import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from utils.db_utils import fetch_all, execute_query

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Администратор - Парацетамол')
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

        self.label_title = QLabel('Панель администратора')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: red;")
        layout.addWidget(self.label_title)

        self.button_manage_users = self.create_button('Управление пользователями')
        self.button_manage_users.clicked.connect(self.manage_users)
        layout.addWidget(self.button_manage_users)

        self.button_view_reports = self.create_button('Просмотр отчетов')
        self.button_view_reports.clicked.connect(self.view_reports)
        layout.addWidget(self.button_view_reports)

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

    def manage_users(self):
        from gui.admin_window import UsersWindow  # Импорт здесь, чтобы избежать циклического импорта
        self.users_window = UsersWindow()
        self.users_window.show()

    def view_reports(self):
        try:
            reports = fetch_all("SELECT * FROM reports")
            from gui.admin_window import ReportsWindow  # Импорт здесь, чтобы избежать циклического импорта
            self.reports_window = ReportsWindow(reports)
            self.reports_window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при просмотре отчетов: {str(e)}')
            print(f"DEBUG: Error fetching reports: {e}")  # Отладочная информация

    def back(self):
        self.close()

class UsersWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление пользователями - Парацетамол')
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

        self.label_title = QLabel('Пользователи')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: red;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.button_add = self.create_button('Добавить пользователя')
        self.button_add.clicked.connect(self.add_user)
        layout.addWidget(self.button_add)

        self.button_delete = self.create_button('Удалить пользователя')
        self.button_delete.clicked.connect(self.delete_user)
        layout.addWidget(self.button_delete)

        self.button_update = self.create_button('Изменить пользователя')
        self.button_update.clicked.connect(self.update_user)
        layout.addWidget(self.button_update)

        self.button_load = self.create_button('Загрузить пользователей')
        self.button_load.clicked.connect(self.load_users)
        layout.addWidget(self.button_load)

        self.button_back = self.create_button('Назад')
        self.button_back.clicked.connect(self.back)
        layout.addWidget(self.button_back)

        self.central_widget.setLayout(layout)
        self.load_users()

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

    def load_users(self):
        users = fetch_all("SELECT * FROM users")
        self.table.setRowCount(len(users))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Логин', 'Пароль', 'Роль'])

        for row_index, row_data in enumerate(users):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def add_user(self):
        # Логика добавления пользователя
        pass

    def delete_user(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для удаления')
            return

        user_id = self.table.item(row, 0).text()
        execute_query("DELETE FROM users WHERE id = ?", (user_id,))
        QMessageBox.information(self, 'Успех', 'Пользователь удален')
        self.load_users()

    def update_user(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку для изменения')
            return

        user_id = self.table.item(row, 0).text()
        # Логика изменения данных пользователя
        pass

    def back(self):
        self.close()

class ReportsWindow(QMainWindow):
    def __init__(self, reports):
        super().__init__()
        self.setWindowTitle('Просмотр отчетов - Парацетамол')
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

        self.label_title = QLabel('Отчеты')
        self.label_title.setFont(QFont('Arial', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: red;")
        layout.addWidget(self.label_title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Дата'])
        self.table.setRowCount(len(reports))

        for row_index, row_data in enumerate(reports):
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
