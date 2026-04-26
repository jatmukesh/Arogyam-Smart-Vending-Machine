#vending_machine/PostDispenseScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from vending_machine.theme import make_header, make_btn, fade_in


class PostDispenseScreen(QWidget):
    def __init__(self, parent_stack, cart_items, total):
        super().__init__()
        self.parent = parent_stack
        self.cart_items = cart_items
        self.total = total

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(make_header("Transaction Complete"))

        layout.addWidget(make_btn("Check Body Vitals"))
        layout.addWidget(make_btn("Close Transaction", bg="#37474F"))

        layout.itemAt(1).widget().clicked.connect(self.go_vitals)
        layout.itemAt(2).widget().clicked.connect(self.go_close)

        fade_in(self)

    def go_vitals(self):
        from vending_machine.BPMonitorScreen import BPMonitorScreen
        screen = BPMonitorScreen(self.parent, self.cart_items, self.total)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    def go_close(self):
        from vending_machine.ReceiptDetailsScreen import ReceiptDetailsScreen
        screen = ReceiptDetailsScreen(self.parent, self.cart_items, self.total)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)