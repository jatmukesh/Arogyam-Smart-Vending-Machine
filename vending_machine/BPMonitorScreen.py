#vending_machine/BPMonitorScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from vending_machine.theme import make_header, make_btn, fade_in
from utils.bp_monitor import measure_bp_and_notify
from utils.email_receipt import send_receipt_email


class BPMonitorScreen(QWidget):
    def __init__(self, parent_stack, cart_items, total):
        super().__init__()
        self.parent = parent_stack
        self.cart_items = cart_items
        self.total = total

        self._build_ui()
        fade_in(self)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(12)

        layout.addWidget(make_header("💓 Check Body Vitals", 20))

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter your name")

        self.age_edit = QLineEdit()
        self.age_edit.setPlaceholderText("Enter your age")

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter your email")

        layout.addWidget(self.name_edit)
        layout.addWidget(self.age_edit)
        layout.addWidget(self.email_edit)

        self.status_label = QLabel("Ready")
        self.result_label = QLabel("")
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)

        start_btn = make_btn("Start BP Measurement")
        home_btn = make_btn("Finish & Go Home", bg="#37474F")

        start_btn.clicked.connect(self.start_bp)
        home_btn.clicked.connect(self.go_home)

        layout.addWidget(start_btn)
        layout.addWidget(home_btn)

    def start_bp(self):
        name = self.name_edit.text().strip()
        age = self.age_edit.text().strip()
        email = self.email_edit.text().strip()

        if not name or not age or not email:
            QMessageBox.warning(self, "Missing Data", "Enter all fields.")
            return

        self.status_label.setText("Measuring...")

        try:
            timestamp, systolic, diastolic, pulse, category = measure_bp_and_notify(
                name, age, email
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.status_label.setText("Done ✅")

        self.result_label.setText(
            f"{timestamp}\nSYS:{systolic} DIA:{diastolic}\nPulse:{pulse}\n{category}"
        )

        try:
            send_receipt_email(
                name=name,
                age=age,
                user_email=email,
                cart_items=self.cart_items,
                total=self.total,
                bp_info={
                    "timestamp": timestamp,
                    "systolic": systolic,
                    "diastolic": diastolic,
                    "pulse": pulse,
                    "category": category,
                }
            )
        except:
            pass

    def go_home(self):
        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)