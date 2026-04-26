
# utils/bp_monitor.py

import serial
import time
import re
import smtplib
import csv
import os
import RPi.GPIO as GPIO

from utils.pdf_report import generate_bp_pdf
from utils.cloud_sync import upload_bp

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from utils.email_config import SENDER_EMAIL, SENDER_PASSWORD


# ---------------- GPIO ----------------

BP_STATUS_PIN = 2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BP_STATUS_PIN, GPIO.IN)


# ---------------- SERIAL ----------------

SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600


# ---------------- FILES ----------------

PDF_FILE = "bp_report.pdf"
BP_LOG_FILE = "bp_log.csv"


# ---------------- CSV INIT ----------------

if not os.path.exists(BP_LOG_FILE):

    with open(BP_LOG_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Timestamp",
            "Name",
            "Age",
            "Email",
            "Systolic",
            "Diastolic",
            "Pulse",
            "Category"
        ])


# ---------------- EMAIL ----------------

def _send_bp_email(
    name,
    age,
    user_email,
    timestamp,
    systolic,
    diastolic,
    pulse,
    category
):

    msg = MIMEMultipart()

    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email
    msg["Subject"] = f"Blood Pressure Report - {category}"


    body = f"""Hello {name},

Your blood pressure test was recorded.

Time: {timestamp}

Systolic : {systolic}
Diastolic: {diastolic}
Pulse    : {pulse}
Category : {category}

PDF attached.

Regards,
Arogyam
"""

    msg.attach(MIMEText(body, "plain"))


    part = MIMEBase("application", "octet-stream")

    with open(PDF_FILE, "rb") as f:
        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        'attachment; filename="bp_report.pdf"'
    )

    msg.attach(part)


    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    server.sendmail(SENDER_EMAIL, user_email, msg.as_string())

    server.quit()


# ---------------- MAIN ----------------

def measure_bp_and_notify(name: str, age: str, user_email: str):

    print("Waiting for BP data...")

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


    while True:

        response = ser.readline().decode("ASCII", errors="ignore").strip()

        if not response:
            continue

        print("RAW UART:", response)


        numbers = re.findall(r"[0-9]+", response)

        if len(numbers) < 3:
            continue


        systolic = int(numbers[0])
        diastolic = int(numbers[1])
        pulse = int(numbers[2])


        date_str = time.strftime("%d-%m-%Y")
        time_str = time.strftime("%H:%M:%S")

        timestamp = f"{date_str} {time_str}"


        # ---------- CATEGORY ----------

        if systolic < 90 and diastolic < 60:
            category = "Hypotension"

        elif 120 < systolic < 139 and 80 < diastolic < 90:
            category = "Prehypertension"

        elif 140 < systolic < 159 and 90 < diastolic < 99:
            category = "Stage 1 Hypertension"

        elif 160 < systolic < 179 and 100 < diastolic < 109:
            category = "Stage 2 Hypertension"

        elif systolic > 180 and diastolic > 110:
            category = "Hypertensive Crisis"

        else:
            category = "Normal"


        # ---------- PDF ----------

        generate_bp_pdf(
            PDF_FILE,
            name,
            age,
            user_email,
            timestamp,
            systolic,
            diastolic,
            pulse,
            category
        )


        # ---------- CSV ----------

        with open(BP_LOG_FILE, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                timestamp,
                name,
                age,
                user_email,
                systolic,
                diastolic,
                pulse,
                category
            ])


        # ---------- CLOUD ----------

        try:

            upload_bp({
                "date": date_str,
                "time": time_str,
                "name": name,
                "email": user_email,
                "systolic": systolic,
                "diastolic": diastolic,
                "pulse": pulse,
                "category": category
            })

        except Exception as e:

            print("BP upload failed:", e)


        # ---------- EMAIL ----------

        _send_bp_email(
            name,
            age,
            user_email,
            timestamp,
            systolic,
            diastolic,
            pulse,
            category
        )


        print("BP Completed")

        return timestamp, systolic, diastolic, pulse, category


