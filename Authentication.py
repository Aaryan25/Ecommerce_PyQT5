from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Database import register_user,validate_user


class RegisterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Registration fields
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText("Password")

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)

        self.back_button = QPushButton("Back to Login", self)
        self.back_button.clicked.connect(self.go_to_login)

        # Adding widgets to layout
        layout.addWidget(QLabel("Register"))
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def go_to_login(self):
        """Switch back to the login screen."""
        self.parent.switch_to_login()

    def register_user(self):
        """Handle user registration."""
        username = self.username_field.text()
        password = self.password_field.text()

        if username and password:
            if register_user(username, password):
                QMessageBox.information(self, "Success", "Account created successfully!")
                self.go_to_login()
            else:
                QMessageBox.warning(self, "Error", "Username already exists.")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Username and Password fields
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText("Password")

        # Buttons
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton("Create Account", self)
        self.register_button.clicked.connect(self.go_to_register)

        # Adding widgets to layout
        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def go_to_register(self):
        """Switch to the registration screen."""
        self.parent.switch_to_register()

    def handle_login(self):
        """Handle user login (authentication logic here)."""
        username = self.username_field.text()
        password = self.password_field.text()
        self.user_id,self.role,self.username= validate_user(username,password)
        if self.role == "admin":  # Example login logic
            self.parent.load_user_screen(self.role)
            QMessageBox.information(self, "Login Successful", "Welcome, Admin!")
        else:
            self.parent.load_user_screen(self.role)
            QMessageBox.information(self, "Login Successful", "Welcome, back!")
