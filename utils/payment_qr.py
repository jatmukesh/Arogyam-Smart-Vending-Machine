# utils/payment_qr.py

"""
💳 UPI QR Code Generator

This module generates a QR code for UPI payments using a configurable UPI ID
and payee name.

⚠️ IMPORTANT:
- Replace UPI_ID with your own valid UPI ID before using this project
- Replace PAYEE_NAME with the name linked to your UPI account
- Do NOT commit real payment credentials to public repositories
- Keep this file generic if sharing the project

🔧 UPI Link Format:
upi://pay?pa=<UPI_ID>&pn=<PAYEE_NAME>&am=<AMOUNT>&cu=INR

Where:
- pa = payee UPI ID
- pn = payee name
- am = amount (in INR)
- cu = currency (INR)

📌 Notes:
- The amount is dynamically passed while generating the QR
- The generated QR can be scanned using any UPI app (GPay, PhonePe, Paytm, etc.)
"""

import qrcode

# Replace with your UPI ID (example: yourname@bank)
UPI_ID = "your_upi_id"

# Replace with your registered UPI display name
PAYEE_NAME = "Your Custom Name or Business Name"


def generate_qr(amount: float, filename: str = "payment_qr.png") -> str:
    """
    Generate a UPI QR code PNG for the given amount.

    Args:
        amount (float): Payment amount in INR
        filename (str): Output file name for the QR image

    Returns:
        str: Path to the saved QR code image
    """

    # Construct UPI payment deep link
    upi_link = (
        f"upi://pay?"
        f"pa={UPI_ID}&"
        f"pn={PAYEE_NAME}&"
        f"am={amount}&"
        f"cu=INR"
    )

    # Generate QR code from UPI link
    img = qrcode.make(upi_link)

    # Save QR code as image file
    img.save(filename)

    return filename