#vending_machine/HomeScreen.py


from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from vending_machine.theme import make_header, make_subheader, make_btn, fade_in


class HomeScreen(QWidget):
    def __init__(self, parent_stack):
        super().__init__()
        self.parent = parent_stack

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        layout.addWidget(make_header("Arogyam Smart Vending Machine", 22))
        layout.addWidget(make_subheader("Choose how you want to proceed"))

        layout.addWidget(make_btn("Enter Symptoms"))
        layout.addWidget(make_btn("Select Medicine"))
        layout.addWidget(make_btn("Place Prescription (OCR)"))
        layout.addWidget(make_btn("Admin Panel", bg="#37474F"))

        # Connect buttons AFTER creation
        layout.itemAt(2).widget().clicked.connect(self.open_symptom_flow)
        layout.itemAt(3).widget().clicked.connect(self.open_select_medicine_flow)
        layout.itemAt(4).widget().clicked.connect(self.open_ocr_flow)
        layout.itemAt(5).widget().clicked.connect(self.open_admin_panel)

        fade_in(self)

    def open_symptom_flow(self):
        from vending_machine.SymptomScreen import SymptomScreen
        screen = SymptomScreen(self.parent)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    def open_select_medicine_flow(self):
        from vending_machine.SelectMedicineScreen import SelectMedicineScreen
        screen = SelectMedicineScreen(self.parent)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    def open_ocr_flow(self):
        from vending_machine.OCRScreen import OCRScreen
        screen = OCRScreen(self.parent)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    def open_admin_panel(self):
        from vending_machine.AdminDashboard import AdminDashboard
        self.admin_screen = AdminDashboard()
        self.admin_screen.show()