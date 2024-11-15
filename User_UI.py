from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox)
from Database import get_items, add_to_cart, checkout, get_cart_items

class UserDashboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Dashboard")

        self.items_table = QTableWidget(self)
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Price", "Stock"])
        self.load_items()

        self.cart_btn = QPushButton("Add to Cart", self)
        self.cart_btn.clicked.connect(self.add_to_cart)

        self.checkout_btn = QPushButton("Checkout", self)
        self.checkout_btn.clicked.connect(self.checkout_items)

        layout = QVBoxLayout()
        layout.addWidget(self.items_table)
        layout.addWidget(self.cart_btn)
        layout.addWidget(self.checkout_btn)

        self.setLayout(layout)

    def load_items(self):
        self.items_table.clearContents()
        items = get_items()
        self.items_table.setRowCount(len(items))
        for row, item in enumerate(items):
            for col, data in enumerate(item):
                self.items_table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_to_cart(self):
        selected = self.items_table.currentRow()
        if selected >= 0:
            item_id = int(self.items_table.item(selected, 0).text())
            add_to_cart(self.user_id, item_id, 1)
            QMessageBox.information(self, "Success", "Item added to cart")

    def checkout_items(self):
        checkout(self.user_id)
        QMessageBox.information(self, "Success", "Checkout complete")
