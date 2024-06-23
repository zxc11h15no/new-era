import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from utils.db_utils import fetch_all, fetch_one
import os

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load background image
        self.pixmap = QPixmap("img/pharmacy_background.jpg")

        # Set fixed size based on background image
        self.setFixedSize(self.pixmap.size())

        self.setWindowTitle('Авторизация - Онлайн аптека Парацетамол')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.set_background()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.label_pharmacy_name = QLabel('Парацетамол')
        self.label_pharmacy_name.setFont(QFont('Times New Roman', 28))
        self.label_pharmacy_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pharmacy_name.setStyleSheet("color: red;")
        layout.addWidget(self.label_pharmacy_name)

        self.label_title = QLabel('Вход в систему')
        self.label_title.setFont(QFont('Times New Roman', 20))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: red;")
        layout.addWidget(self.label_title)

        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText('Логин')
        self.input_login.setFont(QFont('Arial', 14))
        self.input_login.setStyleSheet(
            "background-color: #9370DB; color: white; padding: 10px; border-radius: 15px;"
        )
        layout.addWidget(self.input_login)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Пароль')
        self.input_password.setFont(QFont('Arial', 14))
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setStyleSheet(
            "background-color: #9370DB; color: white; padding: 10px; border-radius: 15px;"
        )
        layout.addWidget(self.input_password)

        self.button_login = QPushButton('Войти')
        self.button_login.setFont(QFont('Arial', 16))
        self.button_login.setStyleSheet(
            "background-color: #9370DB; color: white; border-radius: 15px; padding: 10px;"
        )
        self.button_login.clicked.connect(self.check_credentials)
        layout.addWidget(self.button_login)

        self.central_widget.setLayout(layout)

    def set_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(self.pixmap))
        self.setPalette(palette)

    def check_credentials(self):
        login = self.input_login.text().strip()
        password = self.input_password.text().strip()

        print(f"DEBUG: Input login: {login}, Input password: {password}")  # Отладочная информация

        try:
            # Дополнительная отладочная информация
            print("DEBUG: Connecting to database...")

            # Проверка всех записей в таблице users
            all_users = fetch_all("SELECT id, login, password, post_id FROM users")
            print(f"DEBUG: All users: {all_users}")  # Отладочная информация

            # Выполнение запроса для конкретного пользователя
            results = fetch_all("SELECT id, post_id, password FROM users WHERE login=?", (login,))

            print("DEBUG: SQL query executed.")
            print(f"DEBUG: Results of fetch_all: {results}")  # Отладочная информация
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка подключения к базе данных: {str(e)}')
            print(f"DEBUG: Database connection error: {e}")  # Отладочная информация
            return

        if results:
            # Выберите первую запись из результатов
            result = results[0]
            user_id, post_id, stored_password = result
            print(
                f"DEBUG: Retrieved user_id={user_id}, post_id={post_id}, stored_password={stored_password}")  # Отладочная информация
            if password == stored_password:  # Простое сравнение строк для незашифрованных паролей
                if post_id == 1:
                    from gui.admin_window import AdminWindow  # Импорт здесь, чтобы избежать циклического импорта
                    self.admin_window = AdminWindow()
                    self.admin_window.show()
                elif post_id == 2:
                    from gui.user_window import UserWindow  # Импорт здесь, чтобы избежать циклического импорта
                    self.user_window = UserWindow(user_id)
                    self.user_window.show()
                elif post_id == 3:
                    from gui.employee_window import EmployeeWindow  # Импорт здесь, чтобы избежать циклического импорта
                    self.employee_window = EmployeeWindow()
                    self.employee_window.show()
                self.hide()
            else:
                print("DEBUG: Password mismatch")  # Отладочная информация
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
        else:
            print("DEBUG: No user found")  # Отладочная информация
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

    def back_to_login(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
