from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog,
                             QMessageBox, QComboBox)
from PyQt5.QtGui import QPixmap
from Database import add_item, get_items, delete_item, update_item

class AdminDashboard(QWidget):
    def __init__(self,user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Admin Dashboard")

        # UI Components
        self.item_name = QLineEdit(self)
        self.item_desc = QLineEdit(self)
        self.item_price = QLineEdit(self)
        self.item_stock = QLineEdit(self)
        self.image_path = None

        self.image_btn = QPushButton("Select Image", self)
        self.image_btn.clicked.connect(self.select_image)

        self.add_btn = QPushButton("Add Item", self)
        self.add_btn.clicked.connect(self.add_item)

        self.items_table = QTableWidget(self)
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Price", "Stock"])

        self.load_items()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Item Name:"))
        layout.addWidget(self.item_name)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.item_desc)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.item_price)
        layout.addWidget(QLabel("Stock:"))
        layout.addWidget(self.item_stock)
        layout.addWidget(self.image_btn)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.items_table)

        self.setLayout(layout)

    def select_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if self.image_path:
            QMessageBox.information(self, "Selected", "Image selected successfully")

    def add_item(self):
        name = self.item_name.text()
        desc = self.item_desc.text()
        price = float(self.item_price.text())
        stock = int(self.item_stock.text())
        if name and desc and self.image_path:
            add_item(name, desc, price, stock, self.image_path)
            QMessageBox.information(self, "Success", "Item added successfully")
            self.load_items()
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields")

    def load_items(self):
        self.items_table.clearContents()
        items = get_items()
        self.items_table.setRowCount(len(items))
        for row, item in enumerate(items):
            for col, data in enumerate(item):
                self.items_table.setItem(row, col, QTableWidgetItem(str(data)))
