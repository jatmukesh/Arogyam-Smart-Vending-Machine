"""
vending_machine/theme.py
========================
Global styling, widgets, and animations for the GUI.
"""

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsOpacityEffect, QPushButton, QLabel, QFrame, QWidget
)

# ── Colors ───────────────────────────────────────────────────

BG_DARK    = "#0A1628"
BG_MAIN    = BG_DARK        # ✅ alias for compatibility
BG_CARD    = "#0F2035"
BG_ITEM    = "#12243A"

ACCENT     = "#00BCD4"
ACCENT_LT  = "#4FC3F7"

GREEN      = "#2E7D32"
GREEN_LT   = "#81C784"

ORANGE     = "#E65100"
ORANGE_LT  = "#FFB74D"

RED        = "#C62828"
RED_LT     = "#EF9A9A"

BLUE       = "#1565C0"
BLUE_LT    = "#1976D2"

TXT_PRI    = "#E0E0E0"
TXT_MAIN   = TXT_PRI        # ✅ alias
TXT_SEC    = "#78909C"

# ── Global Stylesheet ─────────────────────────────────────────

APP_STYLESHEET = f"""
QWidget {{
    font-family: "Segoe UI", Arial;
    background-color: {BG_DARK};
    color: {TXT_PRI};
}}

QPushButton {{
    background-color: {BLUE};
    color: white;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {BLUE_LT};
}}

QPushButton:pressed {{
    background-color: #0D47A1;
}}

QPushButton:disabled {{
    background-color: #1A2A3A;
    color: #546E7A;
}}

QLineEdit {{
    background-color: {BG_CARD};
    border: 1px solid #1E3A5F;
    border-radius: 8px;
    padding: 8px;
}}

QLineEdit:focus {{
    border: 1px solid {ACCENT};
}}

QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 2px solid {ACCENT};
    border-radius: 4px;
}}

QCheckBox::indicator:checked {{
    background: {ACCENT};
}}

QSpinBox {{
    background-color: {BG_CARD};
    border-radius: 6px;
    padding: 4px;
}}
"""

# ── UI Helpers ────────────────────────────────────────────────

def make_header(text: str, size: int = 22):
    lbl = QLabel(text)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setFont(QFont("Segoe UI", size, QFont.Bold))
    lbl.setStyleSheet(f"color: {ACCENT_LT};")
    return lbl


def make_subheader(text: str, size: int = 13):
    lbl = QLabel(text)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setFont(QFont("Segoe UI", size))
    lbl.setStyleSheet(f"color: {TXT_SEC};")
    return lbl


def make_btn(text: str, bg: str = BLUE, hover: str = BLUE_LT, height: int = 50):
    btn = QPushButton(text)
    btn.setMinimumHeight(height)
    btn.setFont(QFont("Segoe UI", 13, QFont.Bold))

    btn.setStyleSheet(f"""
        QPushButton {{
            background: {bg};
            color: white;
            border-radius: 10px;
        }}
        QPushButton:hover {{
            background: {hover};
        }}
    """)
    return btn


def make_separator():
    sep = QFrame()
    sep.setFrameShape(QFrame.HLine)
    sep.setStyleSheet("color: #1E3A5F;")
    return sep


# ── Animation ────────────────────────────────────────────────

def fade_in(widget: QWidget, duration: int = 300):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()

    widget._anim = anim  # prevent garbage collection


# ── Spinner ──────────────────────────────────────────────────

class Spinner(QWidget):
    def __init__(self, parent=None, size=60, color=ACCENT):
        super().__init__(parent)
        self.angle = 0
        self.color = QColor(color)
        self.setFixedSize(size, size)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

    def start(self):
        self.timer.start(30)

    def stop(self):
        self.timer.stop()

    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(self.color, 4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        rect = self.rect().adjusted(5, 5, -5, -5)
        painter.drawArc(rect, self.angle * 16, 270 * 16)


# ── Pulse Dot ────────────────────────────────────────────────

class PulseDot(QLabel):
    def __init__(self, on_color=GREEN_LT, off_color=TXT_SEC):
        super().__init__("●")
        self.on = on_color
        self.off = off_color
        self.state = True

        self.setFont(QFont("Segoe UI", 16))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.blink)
        self.apply()

    def start(self):
        self.timer.start(600)

    def stop(self):
        self.timer.stop()

    def blink(self):
        self.state = not self.state
        self.apply()

    def apply(self):
        color = self.on if self.state else self.off
        self.setStyleSheet(f"color: {color}; background: transparent;")


# ── Card Container ───────────────────────────────────────────

class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {BG_CARD};
                border-radius: 12px;
                border: 1px solid #1E3A6A;
            }}
        """)