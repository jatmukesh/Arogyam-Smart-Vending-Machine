#vending_machine/PaymentModeScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from vending_machine.theme import make_header, make_btn, fade_in
from utils.payment_qr import generate_qr


class PaymentModeScreen(QWidget):
    def __init__(self, parent_stack, cart_items):
        super().__init__()
        self.parent = parent_stack
        self.cart_items = cart_items
        self.total = sum(i["price"] * i["qty"] for i in cart_items)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(make_header("Payment"))

        total_lbl = QLabel(f"Total: ₹ {self.total}")
        total_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(total_lbl)

        wallet_btn = make_btn("Vendz Wallet")
        qr_btn = make_btn("UPI QR")
        done_btn = make_btn("Payment Completed", bg="#2E7D32")
        back_btn = make_btn("Back", bg="#37474F")

        wallet_btn.clicked.connect(self.pay_wallet)
        qr_btn.clicked.connect(self.show_qr)
        done_btn.clicked.connect(self.complete)
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(wallet_btn)
        layout.addWidget(qr_btn)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_label)

        layout.addWidget(done_btn)
        layout.addWidget(back_btn)

        fade_in(self)

    def pay_wallet(self):
        QMessageBox.information(self, "Wallet", "Simulated payment success.")

    def show_qr(self):
        file = generate_qr(self.total, "payment_qr.png")
        pixmap = QPixmap(file)
        self.qr_label.setPixmap(pixmap.scaled(250, 250))

    def complete(self):
        from vending_machine.DispenseScreen import DispenseScreen
        screen = DispenseScreen(self.parent, self.cart_items, self.total)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    def go_back(self):
        from vending_machine.CartScreen import CartScreen
        base = [{"name": i["name"], "price": i["price"]} for i in self.cart_items]
        screen = CartScreen(self.parent, base)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)