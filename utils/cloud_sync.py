

# utils/cloud_sync.py

import gspread
from google.oauth2.service_account import Credentials


SHEET_NAME = "Arogyam_Machine_Logs"
KEY_FILE = "google_key.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# ---------------- AUTH ----------------

def get_client():

    creds = Credentials.from_service_account_file(
        KEY_FILE,
        scopes=SCOPES
    )

    return gspread.authorize(creds)


# ---------------- PURCHASE LOG ----------------

def upload_purchase(data: dict):

    client = get_client()

    sheet = client.open(SHEET_NAME).worksheet("purchase_log")

    row = [
        data.get("date", ""),
        data.get("time", ""),
        data.get("name", ""),
        data.get("email", ""),
        data.get("medicine", ""),
        data.get("amount", ""),
        data.get("vitals", "No"),
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")

    print("Purchase uploaded to Sheets")


# ---------------- BP LOG ----------------

def upload_bp(data: dict):

    client = get_client()

    sheet = client.open(SHEET_NAME).worksheet("bp_vital_log")

    row = [
        data.get("date", ""),
        data.get("time", ""),
        data.get("name", ""),
        data.get("email", ""),
        data.get("systolic", ""),
        data.get("diastolic", ""),
        data.get("pulse", ""),
        data.get("category", ""),
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")

    print("BP uploaded to Sheets")


