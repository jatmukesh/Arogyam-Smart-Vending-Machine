#vending_machine/DispenseScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from vending_machine.theme import make_header, make_btn, fade_in, Spinner


class DispenseScreen(QWidget):
    def __init__(self, parent_stack, cart_items, total):
        super().__init__()
        self.parent = parent_stack
        self.cart_items = cart_items
        self.total = total

        self._build_ui()
        fade_in(self)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(make_header("Dispensing Medicines..."))

        self.spinner = Spinner()
        self.spinner.start()
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        info = QLabel("Please wait while medicines are dispensed")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        next_btn = make_btn("Continue")
        next_btn.clicked.connect(self.go_next)
        layout.addWidget(next_btn)

    def go_next(self):
        from vending_machine.PostDispenseScreen import PostDispenseScreen
        screen = PostDispenseScreen(self.parent, self.cart_items, self.total)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)