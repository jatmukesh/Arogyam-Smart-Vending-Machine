from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt

from vending_machine.theme import make_header, make_subheader, make_btn, fade_in


class CartScreen(QWidget):
    def __init__(self, parent_stack, initial_items):
        super().__init__()
        self.parent = parent_stack
        self.items = initial_items
        self.row_widgets = []
        self.total_amount = 0

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(14)

        main_layout.addWidget(make_header("Your Cart"))
        main_layout.addWidget(make_subheader("Adjust quantity before checkout"))

        # 🔥 ITEM CARDS
        for item in self.items:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #0F2035;
                    border-radius: 12px;
                    border: 1px solid #1E3A5F;
                }
            """)

            row = QHBoxLayout(card)
            row.setContentsMargins(15, 12, 15, 12)

            # Medicine name
            name_label = QLabel(item["name"])
            name_label.setStyleSheet("font-size: 15px; font-weight: bold;")

            # Price
            price_label = QLabel(f"₹ {item['price']}")
            price_label.setStyleSheet("""
                color: #4FC3F7;
                font-size: 14px;
                font-weight: bold;
            """)

            # 🔥 QUANTITY CONTROL (NEW)
            qty_layout = QHBoxLayout()
            qty_layout.setSpacing(6)

            # ➖ Minus button
            minus_btn = QPushButton("-")
            minus_btn.setFixedSize(40, 40)
            minus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #C62828;
                    color: white;
                    font-size: 18px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #EF5350;
                }
            """)

            # Quantity display
            qty_label = QLabel("0")
            qty_label.setAlignment(Qt.AlignCenter)
            qty_label.setFixedWidth(40)
            qty_label.setStyleSheet("""
                background-color: #12243A;
                border: 2px solid #00BCD4;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            """)

            # ➕ Plus button
            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(40, 40)
            plus_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E7D32;
                    color: white;
                    font-size: 18px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #66BB6A;
                }
            """)

            # Store quantity
            row_data = {
                "item": item,
                "qty": 0,
                "label": qty_label
            }

            # Button logic
            def make_increment(rd):
                def inc():
                    if rd["qty"] < 10:
                        rd["qty"] += 1
                        rd["label"].setText(str(rd["qty"]))
                        self.update_total()
                return inc

            def make_decrement(rd):
                def dec():
                    if rd["qty"] > 0:
                        rd["qty"] -= 1
                        rd["label"].setText(str(rd["qty"]))
                        self.update_total()
                return dec

            plus_btn.clicked.connect(make_increment(row_data))
            minus_btn.clicked.connect(make_decrement(row_data))

            qty_layout.addWidget(minus_btn)
            qty_layout.addWidget(qty_label)
            qty_layout.addWidget(plus_btn)

            # Layout arrangement
            row.addWidget(name_label)
            row.addStretch()
            row.addWidget(price_label)
            row.addSpacing(20)
            row.addLayout(qty_layout)

            main_layout.addWidget(card)
            self.row_widgets.append(row_data)

        # 🔥 TOTAL
        self.total_label = QLabel("Total: ₹ 0")
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00E676;
        """)
        main_layout.addWidget(self.total_label)

        # Buttons
        back_btn = make_btn("Back", bg="#37474F")
        proceed_btn = make_btn("Proceed to Payment")

        back_btn.clicked.connect(self.go_back)
        proceed_btn.clicked.connect(self.proceed_to_payment)

        main_layout.addWidget(back_btn)
        main_layout.addWidget(proceed_btn)

        self.update_total()
        fade_in(self)

    def update_total(self):
        total = 0
        for row in self.row_widgets:
            total += row["item"]["price"] * row["qty"]

        self.total_amount = total
        self.total_label.setText(f"Total: ₹ {total}")

    def go_back(self):
        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)

    def proceed_to_payment(self):
        cart_items = []

        for row in self.row_widgets:
            if row["qty"] > 0:
                cart_items.append({
                    "name": row["item"]["name"],
                    "price": row["item"]["price"],
                    "qty": row["qty"]
                })

        if not cart_items:
            QMessageBox.warning(self, "Empty Cart",
                                "Please select at least one medicine.")
            return

        from vending_machine.PaymentModeScreen import PaymentModeScreen
        screen = PaymentModeScreen(self.parent, cart_items)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)