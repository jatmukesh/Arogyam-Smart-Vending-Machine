#vending_machine/SelectMedicineScreen.py

# vending_machine/SelectMedicineScreen.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt

from vending_machine.theme import (
    make_header, make_btn, make_separator,
    BG_MAIN, BG_CARD, ACCENT, TXT_MAIN, TXT_SEC
)


class MedicineCard(QFrame):
    def __init__(self, med_data):
        super().__init__()
        self.med_data = med_data
        self.selected = False

        self.setFixedSize(240, 90)
        self.setStyleSheet(self.get_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        self.name_lbl = QLabel(med_data["name"])
        self.name_lbl.setStyleSheet(f"color:{TXT_MAIN}; font-size:13px; font-weight:600;")

        self.price_lbl = QLabel(f"₹ {med_data['price']}")
        self.price_lbl.setStyleSheet(f"color:{TXT_SEC}; font-size:12px;")

        layout.addWidget(self.name_lbl)
        layout.addWidget(self.price_lbl)

    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.setStyleSheet(self.get_style())

    def get_style(self):
        if self.selected:
            return f"""
                QFrame {{
                    background-color: #0F2A44;
                    border: 2px solid {ACCENT};
                    border-radius: 12px;
                }}
            """
        else:
            return f"""
                QFrame {{
                    background-color: {BG_CARD};
                    border: 1px solid #1E3A5F;
                    border-radius: 12px;
                }}
                QFrame:hover {{
                    border: 1px solid {ACCENT};
                }}
            """


class SelectMedicineScreen(QWidget):
    def __init__(self, parent_stack):
        super().__init__()
        self.parent = parent_stack

        self.setWindowTitle("Select Medicine")
        self.setStyleSheet(f"background-color: {BG_MAIN};")

        self.cards = []

        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)

        main_layout.addWidget(make_header("💊 Select Medicines", size=22))
        main_layout.addWidget(make_separator())

        subtitle = QLabel("Tap medicines to add them to your cart")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color:{TXT_SEC}; font-size:13px;")
        main_layout.addWidget(subtitle)

        # ---------------- MEDICINE GRID ----------------
        grid = QGridLayout()
        grid.setSpacing(15)

        self.medicine_catalog = [
            {"name": "Paracetamol 650 mg", "price": 20},
            {"name": "Ibuprofen 200 mg", "price": 25},
            {"name": "Cetirizine 10 mg", "price": 15},
            {"name": "Azithromycin 500 mg", "price": 40},
            {"name": "Dextromethorphan Syrup", "price": 60},
            {"name": "Pantoprazole 40 mg", "price": 30},
            {"name": "Simethicone 80 mg", "price": 25},
            {"name": "ORS Sachet", "price": 18},
            {"name": "Loperamide 2 mg", "price": 22},
            {"name": "Lactulose Syrup", "price": 80},
        ]

        row, col = 0, 0
        for med in self.medicine_catalog:
            card = MedicineCard(med)
            self.cards.append(card)

            grid.addWidget(card, row, col)

            col += 1
            if col == 3:  # 3 cards per row
                col = 0
                row += 1

        main_layout.addLayout(grid)

        # ---------------- BUTTONS ----------------
        main_layout.addStretch()
        main_layout.addWidget(make_separator())

        add_btn = make_btn("🛒 Add to Cart", height=48)
        add_btn.clicked.connect(self.go_to_cart)

        back_btn = make_btn("⬅ Back to Home", bg="#37474F", hover="#455A64", height=48)
        back_btn.clicked.connect(self.go_home)

        main_layout.addWidget(add_btn)
        main_layout.addWidget(back_btn)

    # ---------------- LOGIC (UNCHANGED) ----------------

    def go_to_cart(self):
        selected_items = []

        for card in self.cards:
            if card.selected:
                selected_items.append(card.med_data)

        if not selected_items:
            QMessageBox.warning(self, "No Medicines Selected",
                                "Please select at least one medicine.")
            return

        from vending_machine.CartScreen import CartScreen
        cart = CartScreen(self.parent, selected_items)
        self.parent.addWidget(cart)
        self.parent.setCurrentWidget(cart)

    def go_home(self):
        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)