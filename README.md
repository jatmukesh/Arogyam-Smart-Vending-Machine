# 🏥 Arogyam – Smart Medicine Vending Machine

## 📌 Overview

**Arogyam Smart Medicine Vending Machine** is an AI-powered, IoT-enabled healthcare system designed to provide **instant, contactless access to essential medicines**.

The system integrates **OCR-based prescription recognition, symptom-based recommendation, digital payment, and automated dispensing** into a single intelligent platform.

Built using **Raspberry Pi**, the machine functions as a **24×7 automated pharmacy**, especially useful in hospitals, campuses, and rural areas. 

---

## 🎯 Objectives

* Provide quick and contactless access to medicines
* Implement **OCR-based prescription reading**
* Enable **UPI-based digital payments**
* Automate dispensing using embedded systems
* Maintain real-time inventory and transaction logs
* Enhance healthcare accessibility in remote areas 

---

## 🚀 Key Features

### 🧠 AI-Based Medicine Recommendation

* Symptom-based medicine suggestion using medical APIs
* Intelligent decision-making using user input + vitals

### 📄 OCR Prescription Recognition

* YOLOv8 for text detection
* TrOCR for handwriting recognition
* Automatic extraction and validation of medicines

### 🖥️ Touchscreen GUI

* Built using PyQt5
* Multiple interaction modes:

  * Symptom-based
  * Direct selection
  * Prescription scan

### 💳 Digital Payment System

* Dynamic **UPI QR code generation**
* Secure and cashless transactions

### 📦 Automated Dispensing

* Stepper motor (28BYJ-48) based mechanism
* Controlled using Raspberry Pi
* Flap + limit switch for accuracy

### ❤️ Health Monitoring

* Blood pressure monitoring
* Optional vital parameter tracking

### ☁️ Cloud Logging

* Google Sheets integration
* Real-time transaction & inventory tracking

### 🧾 Digital Receipt

* Email-based receipt generation

### 👨‍💻 Admin Dashboard

* Inventory management
* Sales analytics
* System monitoring 

---

## 🏗️ System Architecture

```text
User Interaction (Touchscreen GUI)
        ↓
Input Modes:
  - Symptoms
  - Direct Selection
  - OCR Prescription Scan
        ↓
AI/ML Processing (YOLOv8 + TrOCR + APIs)
        ↓
Medicine Validation (Database Matching)
        ↓
Payment (UPI QR Code)
        ↓
Dispensing Mechanism (Stepper Motor)
        ↓
Inventory Update + Cloud Logging + Receipt
```

---

## ⚙️ Technologies Used

### 💻 Software

* Python
* PyQt5 (GUI)
* OpenCV (Image Processing)
* YOLOv8 (Text Detection)
* TrOCR (Handwriting Recognition)
* RapidFuzz (Medicine Matching)
* Flask (Backend API)
* SQLite / Google Sheets (Database & Logging)
* smtplib (Email Service)

### 🔧 Hardware

* Raspberry Pi 3/5
* 7-inch Touchscreen Display
* MLX90614 Temperature Sensor
* Blood Pressure Sensor
* Raspberry Pi Camera Module
* Stepper Motor (28BYJ-48) + ULN2003 Driver
* Load Cell with HX711 (optional)
* Limit Switch (Flap mechanism) 

---

## 🔄 Working / Workflow

1. User interacts with touchscreen interface
2. Selects mode:

   * Symptoms
   * Direct medicine
   * Prescription scan
3. OCR extracts medicine (if prescription used)
4. AI suggests or validates medicines
5. User confirms selection
6. QR code generated for payment
7. Payment verified
8. Medicine dispensed automatically
9. Inventory updated
10. Optional email receipt sent 

---

## 📂 Project Structure

```bash
## 📂 Project Structure
Arogyam/
│
├── .venv/                     # Virtual environment (ignored in Git)
├── captured_images/          # Stored prescription images
│
├── client/                   # Hardware interaction layer
│   ├── camera.py             # Camera preview & image capture
│   ├── uploader.py           # Image upload/handling logic
│
├── utils/                    # Core backend logic modules
│   ├── bp_monitor.py         # Blood pressure monitoring
│   ├── cloud_sync.py         # Google Sheets / cloud logging
│   ├── dispense_controller.py# Motor control for dispensing
│   ├── email_config.py       # Email setup configuration
│   ├── email_receipt.py      # Sending digital receipts
│   ├── ocr_inference.py      # OCR pipeline (YOLOv8 + TrOCR)
│   ├── payment_qr.py         # QR code generation
│   ├── pdf_report.py         # Report generation
│   ├── receipt_pdf.py        # Receipt PDF creation
│
├── vending_machine/          # Main application (UI + flow)
│   ├── AdminDashboard.py         # Admin panel for monitoring system
│                                 # Displays inventory, sales analytics, logs
│   ├── BPMonitorScreen.py        # Blood pressure monitoring screen
│                                 # Shows systolic, diastolic, pulse readings
│   ├── CartScreen.py             # Cart interface
│                                 # Displays selected medicines, quantity, total price
│   ├── DispenseScreen.py         # Dispensing process screen
│                                 # Triggers motor and shows dispensing status
│   ├── HomeScreen.py             # Main entry UI screen
│                                 # Navigation: Symptoms | Select Medicine | OCR | Admin
│   ├── OCRScreen.py              # Prescription scanning screen
│                                 # Captures image → runs OCR → extracts medicines
│   ├── PaymentModeScreen.py      # Payment interface
│                                 # Generates UPI QR and handles payment flow
│   ├── PostDispenseScreen.py     # Transaction completion screen
│                                 # Confirms success and next actions
│   ├── ReceiptDetailsScreen.py   # Receipt input screen
│                                 # Takes email for sending digital receipt
│   ├── SelectMedicineScreen.py   # Direct medicine selection screen
│                                 # Lists medicines from inventory
│   ├── SymptomScreen.py          # Symptom-based selection screen
│                                 # Suggests medicines based on symptoms
|
│
├── bp_log.csv                # Stored BP readings
├── purchase_log.csv          # Transaction records
├── payment_qr.png            # Generated QR sample
├── purchase_receipt.pdf      # Sample receipt
├── bp_report.pdf             # Generated BP report
│
├── google_key.json           # Google API credentials
├── main.py                   # Main entry point
├── packages_setup.txt        # Setup instructions
├── req_txt                   # Requirements file
├── README.md                 # Project documentation
```


## 🧠 Architecture Insight

The project follows a **modular layered architecture**:

* **client/** → Handles hardware (camera input)
* **utils/** → Core processing (OCR, payment, email, cloud, dispensing)
* **vending_machine/** → User interface + workflow control
* **main.py** → Connects everything and runs the system

This separation ensures:

* Easy debugging
* Scalable design
* Clean integration of AI + IoT modules

---

```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/Arogyam.git
cd Arogyam
```

### 2️⃣ Install Dependencies

```bash
pip install pyqt5 flask opencv-python ultralytics transformers rapidfuzz pandas reportlab gspread oauth2client
```

### 3️⃣ Add Model Files

Place inside `models/`:

* YOLOv8 model (`yolov8n.pt`)
* TrOCR model
* doctor_classifier.pt

### 4️⃣ Run Application

```bash
python main.py
```

---

## 🧪 Results

* Accurate OCR-based prescription recognition
* Reliable medicine dispensing mechanism
* Successful integration of AI + IoT + Payment system
* Real-time cloud logging and monitoring
* Multi-mode interaction improves usability 

---

## 🌍 Applications

* Hospitals
* Colleges & Campuses
* Railway Stations
* Rural Healthcare Centers
* Pharmacies

---

## 🔮 Future Scope

* Telemedicine integration
* AI-based disease prediction
* Mobile app connectivity
* Multilingual support
* Biometric authentication
* Integration with digital health records 

---

## 👥 Team

* Mukesh Jat
* Mrunmayi Modak
* Ayush Palde
* Piyush Sanap

---

## 🏫 Institute

Xavier Institute of Engineering, Mumbai
Department of Electronics & Telecommunication
University of Mumbai

---

## 📄 License

This project is developed for academic and research purposes.

---

## 💡 Vision

To enable **accessible, automated, and intelligent healthcare** through technology-driven solutions.

---
