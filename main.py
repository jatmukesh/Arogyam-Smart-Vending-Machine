import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from vending_machine.HomeScreen import HomeScreen
from vending_machine.theme import APP_STYLESHEET   # ✅ NEW


def main():
    app = QApplication(sys.argv)

    # ✅ Apply global theme (THIS IS THE MAIN CHANGE)
    app.setStyleSheet(APP_STYLESHEET)

    # Central stack to hold all screens
    stack = QStackedWidget()
    stack.setWindowTitle("Arogyam Smart Medicine Vending Machine")
    stack.resize(800, 480)  # unchanged

    # Start with Home screen
    home = HomeScreen(stack)
    stack.addWidget(home)
    stack.setCurrentWidget(home)

    stack.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()