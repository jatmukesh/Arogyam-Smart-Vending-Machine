# vending_machine/OCRScreen.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

from vending_machine.theme import make_header, make_btn, fade_in, Spinner
from utils.ocr_inference import run_ocr_pipeline

# ✅ Camera functions
from client.camera import (
    start_preview,
    get_frame,
    stop_preview,
    auto_capture_ready,
    capture_image
)

import cv2


class OCRScreen(QWidget):
    def __init__(self, parent_stack):
        super().__init__()
        self.parent = parent_stack
        self.server_url = "http://192.168.1.5:5000"

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        layout.addWidget(make_header("Scan Prescription"))

        self.status = QLabel("📄 Place prescription and start scan")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        # -------- 📷 LIVE CAMERA PREVIEW --------
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(480, 320)
        self.camera_label.setStyleSheet("background-color: black; border-radius: 10px;")
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label)

        self.spinner = Spinner()
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        # -------- BUTTONS --------
        self.scan_btn = make_btn("Start Scan")
        self.capture_btn = make_btn("Capture Now", bg="#00897B")
        self.back_btn = make_btn("Back", bg="#37474F")

        self.capture_btn.setEnabled(False)

        self.scan_btn.clicked.connect(self.start_scan)
        self.capture_btn.clicked.connect(self.manual_capture)
        self.back_btn.clicked.connect(self.go_home)

        layout.addWidget(self.scan_btn)
        layout.addWidget(self.capture_btn)
        layout.addWidget(self.back_btn)

        fade_in(self)

        # Timer for preview loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    # ---------------- START SCAN ----------------

    def start_scan(self):
        self.status.setText("📷 Starting camera...")
        self.scan_btn.setEnabled(False)
        self.capture_btn.setEnabled(True)

        start_preview()
        self.timer.start(30)  # ~30 FPS

    # ---------------- LIVE PREVIEW LOOP ----------------

    def update_frame(self):
        frame = get_frame()
        if frame is None:
            return

        # Convert frame to Qt image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)

        self.camera_label.setPixmap(pixmap.scaled(
            self.camera_label.width(),
            self.camera_label.height(),
            Qt.KeepAspectRatio
        ))

        # -------- AUTO CAPTURE --------
        if auto_capture_ready(frame):
            self.timer.stop()
            self.process_capture(frame)

    # ---------------- MANUAL CAPTURE ----------------

    def manual_capture(self):
        frame = get_frame()
        if frame is None:
            QMessageBox.warning(self, "Error", "Camera not ready")
            return

        self.timer.stop()
        self.process_capture(frame, manual=True)

    # ---------------- PROCESS IMAGE ----------------

    def process_capture(self, frame, manual=False):
        self.status.setText("📷 Processing image...")
        self.spinner.start()
        self.repaint()

        path = capture_image(frame, manual=manual)

        if path is None:
            QMessageBox.warning(self, "Poor Image", "Image not clear. Try again.")
            self.status.setText("⚠️ Try again")
            self.spinner.stop()
            self.timer.start(30)
            return

        # Stop camera after capture
        stop_preview()
        self.timer.stop()

        # -------- OCR --------
        result = run_ocr_pipeline(self.server_url, image_path=path)

        self.spinner.stop()

        if not result["success"]:
            QMessageBox.critical(self, "OCR Error", result["error"])
            self.reset_ui("❌ Failed")
            return

        cart_items = result["cart_items"]

        if not cart_items:
            QMessageBox.warning(self, "No Medicines", "No medicines detected")
            self.reset_ui("⚠️ No results")
            return

        # -------- GO TO CART --------
        from vending_machine.CartScreen import CartScreen
        screen = CartScreen(self.parent, cart_items)
        self.parent.addWidget(screen)
        self.parent.setCurrentWidget(screen)

    # ---------------- RESET ----------------

    def reset_ui(self, message=""):
        self.status.setText(message)
        self.scan_btn.setEnabled(True)
        self.capture_btn.setEnabled(False)
        stop_preview()
        self.timer.stop()
        self.camera_label.clear()

    # ---------------- NAVIGATION ----------------

    def go_home(self):
        self.reset_ui()

        from vending_machine.HomeScreen import HomeScreen
        home = HomeScreen(self.parent)
        self.parent.addWidget(home)
        self.parent.setCurrentWidget(home)