
# utils/email_receipt.py

import smtplib
import csv
import os
import time

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from utils.cloud_sync import upload_purchase
from utils.email_config import SENDER_EMAIL, SENDER_PASSWORD
from utils.receipt_pdf import generate_receipt_pdf


# ---------------- FILES ----------------

PURCHASE_LOG_FILE = "purchase_log.csv"
PDF_RECEIPT_FILE = "purchase_receipt.pdf"


# ---------------- CSV INIT ----------------

if not os.path.exists(PURCHASE_LOG_FILE):

    with open(PURCHASE_LOG_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Timestamp",
            "Name",
            "Age",
            "Email",
            "Total",
            "Items",
            "Vitals"
        ])


# ---------------- MAIN ----------------

def send_receipt_email(
    name,
    age,
    user_email,
    cart_items,
    total,
    bp_info=None
):


    date_str = time.strftime("%d-%m-%Y")
    time_str = time.strftime("%H:%M:%S")

    timestamp = f"{date_str} {time_str}"


    # ---------- PDF ----------

    generate_receipt_pdf(
        PDF_RECEIPT_FILE,
        name,
        age,
        user_email,
        timestamp,
        cart_items,
        total
    )


    # ---------- ITEMS ----------

    items_text = ", ".join(
        [f"{i['name']} x{i['qty']}" for i in cart_items]
    )


    vitals_flag = "Yes" if bp_info else "No"


    # ---------- EMAIL ----------

    msg = MIMEMultipart()

    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email
    msg["Subject"] = "Arogyam Purchase Receipt"


    body = f"""Hello {name},

Transaction Time: {timestamp}

Items Purchased:
{items_text}

Total Paid: Rs.{total}

Vitals Taken: {vitals_flag}

Your PDF receipt is attached.

Regards,
Arogyam
"""

    msg.attach(MIMEText(body, "plain"))


    # ---------- ATTACH PDF ----------

    part = MIMEBase("application", "octet-stream")

    with open(PDF_RECEIPT_FILE, "rb") as f:
        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        'attachment; filename="purchase_receipt.pdf"'
    )

    msg.attach(part)


    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    server.sendmail(SENDER_EMAIL, user_email, msg.as_string())

    server.quit()


    # ---------- CSV ----------

    with open(PURCHASE_LOG_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            timestamp,
            name,
            age,
            user_email,
            total,
            items_text,
            vitals_flag
        ])


    # ---------- CLOUD ----------

    try:

        upload_purchase({
            "date": date_str,
            "time": time_str,
            "name": name,
            "email": user_email,
            "medicine": items_text,
            "amount": total,
            "vitals": vitals_flag
        })

    except Exception as e:

        print("Purchase upload failed:", e)


    print("Receipt completed")
