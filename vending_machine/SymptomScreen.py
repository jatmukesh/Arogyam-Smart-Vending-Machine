#vending_machine/SymptomScreen.py


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QGridLayout
)

from vending_machine.theme import make_header, make_subheader, make_btn, fade_in


class SymptomScreen(QWidget):
    def __init__(self, parent_stack):
        super().__init__()
        self.parent = parent_stack

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(16)

        main_layout.addWidget(make_header("Select Your Symptoms"))
        main_layout.addWidget(make_subheader("Choose all that apply"))

        # Store buttons instead of checkboxes
        self.symptom_buttons = []

        # SAME DATA (UNCHANGED)
        symptom_groups = {
            "Fever / Pain": ["Fever", "Headache", "Body Pain"],
            "Cold / Cough": ["Runny Nose", "Sore Throat", "Dry Cough"],
            "Stomach / Digestion": ["Acidity", "Gas / Bloating", "Loose Motion", "Constipation"]
        }

        # 🔥 GRID LAYOUT
        for group_name, symptoms in symptom_groups.items():

            group_label = QLabel(group_name)
            group_label.setStyleSheet("font-size:16px; font-weight:bold;")
            main_layout.addWidget(group_label)

            grid = QGridLayout()
            grid.setSpacing(12)

            row = 0
            col = 0

            for s in symptoms:
                btn = QPushButton(s)
                btn.setCheckable(True)

                # 🔥 Button Style (toggle effect)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #12243A;
                        border: 2px solid #1E3A5F;
                        border-radius: 12px;
                        padding: 14px;
                        font-size: 13px;
                    }
                    QPushButton:checked {
                        background-color: #00BCD4;
                        color: black;
                        border: 2px solid #00BCD4;
                    }
                """)

                self.symptom_buttons.append(btn)
                grid.addWidget(btn, row, col)

                col += 1
                if col == 3:  # 3 per row
                    col = 0
                    row += 1

            main_layout.addLayout(grid)

        # Buttons
        next_btn = make_btn("Get Suggested Medicines")
        back_btn = make_btn("Back to Home", bg="#37474F")

        next_btn.clicked.connect(self.get_suggestions)
        back_btn.clicked.connect(self.go_home)

        main_layout.addWidget(next_btn)
        main_layout.addWidget(back_btn)

        fade_in(self)

    # SAME LOGIC (just changed how we read selection)
    def get_suggestions(self):
        selected = [btn.text() for btn in self.symptom_buttons if btn.isChecked()]

        if not selected:
            QMessageBox.warning(self, "No Symptoms Selected",
                                "Please select at least one symptom.")
            return

        # SAME mapping
        symptom_to_meds = {
            "Fever": ["Paracetamol 650 mg"],
            "Headache": ["Paracetamol 650 mg", "Ibuprofen 200 mg"],
            "Body Pain": ["Paracetamol 650 mg", "Ibuprofen 200 mg"],
            "Runny Nose": ["Cetirizine 10 mg"],
            "Sore Throat": ["Azithromycin 500 mg", "Paracetamol 650 mg"],
            "Dry Cough": ["Dextromethorphan Syrup"],
            "Acidity": ["Pantoprazole 40 mg"],
            "Gas / Bloating": ["Simethicone 80 mg"],
            "Loose Motion": ["ORS Sachet", "Loperamide 2 mg"],
            "Constipation": ["Lactulose Syrup"]
        }

        suggested_set = set()
        for symptom in selected:
            for med in symptom_to_meds.get(symptom, []):
                suggested_set.add(med)

        if not suggested_set:
            QMessageBox.information(self, "No Suggestions",
                                    "No medicines found.")
            return

        price_map = {
            "Paracetamol 650 mg": 20,
            "Ibuprofen 200 mg": 25,
            "Cetirizine 10 mg": 15,
            "Azithromycin 500 mg": 40,
            "Dextromethorphan Syrup": 60,
            "Pantoprazole 40 mg": 30,
            "Simethicone 80 mg": 25,
            "ORS Sachet": 18,
            "Loperamide 2 mg": 22,
            "Lactulose Syrup": 80,
        }

        suggested_medicines = [
            {"name": m, "price": price_map.get(m, 25)}
            for m in suggested_set
        ]

        from vending_machine.CartScreen import CartScreen
        cart_screen = CartScreen(self.parent, suggested_medicines)
        self.parent.addWidget(cart_screen)
        self.parent.setCurrentWidget(cart_screen)

    def go_home(self):
        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)