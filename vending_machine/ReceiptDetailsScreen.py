#vending_machine/ReceiptDetailsScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox

from vending_machine.theme import make_header, make_btn, fade_in
from utils.email_receipt import send_receipt_email


class ReceiptDetailsScreen(QWidget):
    def __init__(self, parent_stack, cart_items, total):
        super().__init__()
        self.parent = parent_stack
        self.cart_items = cart_items
        self.total = total

        layout = QVBoxLayout(self)

        layout.addWidget(make_header("Enter Details"))

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")

        self.age = QLineEdit()
        self.age.setPlaceholderText("Age")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        layout.addWidget(self.name)
        layout.addWidget(self.age)
        layout.addWidget(self.email)

        send_btn = make_btn("Send Receipt")
        home_btn = make_btn("Cancel", bg="#37474F")

        send_btn.clicked.connect(self.send)
        home_btn.clicked.connect(self.go_home)

        layout.addWidget(send_btn)
        layout.addWidget(home_btn)

        fade_in(self)

    def send(self):
        if not self.name.text() or not self.age.text() or not self.email.text():
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        send_receipt_email(
            name=self.name.text(),
            age=self.age.text(),
            user_email=self.email.text(),
            cart_items=self.cart_items,
            total=self.total,
            bp_info=None
        )

        QMessageBox.information(self, "Done", "Receipt Sent")
        self.go_home()

    def go_home(self):
        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)