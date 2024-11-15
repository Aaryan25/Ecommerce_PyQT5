import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Database import create_db
from Authentication import LoginScreen, RegisterScreen
from Admin_UI import AdminDashboard
from User_UI import UserDashboard

class ECommerceApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.role = None
        self.username = None

        create_db()

        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)

        self.addWidget(self.login_screen)
        self.addWidget(self.register_screen)
        self.setCurrentWidget(self.login_screen)

        self.setWindowTitle("E-Commerce App")
        self.setFixedSize(800, 600)
    def switch_to_register(self):
        """Switch to the registration screen."""
        self.setCurrentWidget(self.register_screen)

    def switch_to_login(self):
        """Switch back to the login screen."""
        self.setCurrentWidget(self.login_screen)
    def load_user_screen(self,role):
        if role == "admin":
            self.admin_dashboard = AdminDashboard(self.user_id)
            self.addWidget(self.admin_dashboard)
            self.setCurrentWidget(self.admin_dashboard)
        else:
            self.user_dashboard = UserDashboard(self.user_id)
            self.addWidget(self.user_dashboard)
            self.setCurrentWidget(self.user_dashboard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ecommerce_app = ECommerceApp()
    ecommerce_app.show()
    sys.exit(app.exec_())
