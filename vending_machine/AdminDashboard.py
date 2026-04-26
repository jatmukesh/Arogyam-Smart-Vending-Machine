#vending_machine/AdminDashboard.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import csv, os

from vending_machine.theme import (
    make_header, make_btn, make_separator, fade_in,
    GREEN_LT, ACCENT_LT, TXT_SEC, BG_CARD
)

PURCHASE_LOG = "purchase_log.csv"
BP_LOG = "bp_log.csv"


class AdminDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Admin Dashboard")
        self.setStyleSheet(f"background: {BG_CARD};")

        self._build_ui()
        self.load_data()
        fade_in(self)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        layout.addWidget(make_header("🔧 Admin Dashboard", size=20))
        layout.addWidget(make_separator())

        self.revenue_label = QLabel()
        self.sales_label = QLabel()
        self.bp_label = QLabel()

        for lbl in (self.revenue_label, self.sales_label, self.bp_label):
            lbl.setFont(QFont("Segoe UI", 15))
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)

        layout.addStretch()
        layout.addWidget(make_separator())

        refresh_btn = make_btn("🔄 Refresh", height=44)
        export_btn = make_btn("📂 Export Logs", bg="#263238", hover="#37474F")
        close_btn = make_btn("❌ Close", bg="#B71C1C", hover="#C62828")

        refresh_btn.clicked.connect(self.load_data)
        export_btn.clicked.connect(self.export_logs)
        close_btn.clicked.connect(self.close)

        layout.addWidget(refresh_btn)
        layout.addWidget(export_btn)
        layout.addWidget(close_btn)

    def load_data(self):
        revenue, sales, bp_tests = 0, 0, 0

        if os.path.exists(PURCHASE_LOG):
            with open(PURCHASE_LOG) as f:
                for row in csv.DictReader(f):
                    try:
                        revenue += float(row.get("Total", 0))
                        sales += 1
                    except:
                        pass

        if os.path.exists(BP_LOG):
            with open(BP_LOG) as f:
                bp_tests = sum(1 for _ in csv.DictReader(f))

        self.revenue_label.setText(f"💰 Total Revenue: ₹ {revenue:.2f}")
        self.sales_label.setText(f"🛒 Total Sales: {sales}")
        self.bp_label.setText(f"❤️ BP Tests: {bp_tests}")

        self.revenue_label.setStyleSheet(f"color: {GREEN_LT};")
        self.sales_label.setStyleSheet(f"color: {ACCENT_LT};")
        self.bp_label.setStyleSheet("color: #EF9A9A;")

    def export_logs(self):
        if not os.path.exists(PURCHASE_LOG) and not os.path.exists(BP_LOG):
            QMessageBox.warning(self, "No Data", "No log files found.")
            return

        QMessageBox.information(
            self,
            "Export",
            "Logs are stored as CSV files in project folder.\nYou can copy them using SCP."
        )