
# utils/receipt_pdf.py

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black, lightgrey


def generate_receipt_pdf(
    filename,
    name,
    age,
    email,
    timestamp,
    cart_items,
    total
):
    """
    Generate PDF purchase receipt
    """

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []


    # Title
    elements.append(
        Paragraph("<b>Arogyam Smart Medicine Vending Machine</b>", styles["Title"])
    )
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("Purchase Receipt", styles["h2"])
    )
    elements.append(Spacer(1, 20))


    # User Info
    info = f"""
    <b>Name:</b> {name}<br/>
    <b>Age:</b> {age}<br/>
    <b>Email:</b> {email}<br/>
    <b>Date & Time:</b> {timestamp}
    """

    elements.append(Paragraph(info, styles["Normal"]))
    elements.append(Spacer(1, 25))


    # Table Header
    data = [["Medicine", "Qty", "Price", "Total"]]


    # Items
    for item in cart_items:
        data.append([
            item["name"],
            str(item["qty"]),
            f"₹{item['price']}",
            f"₹{item['price'] * item['qty']}"
        ])


    # Grand total
    data.append(["", "", "Grand Total", f"₹{total}"])


    table = Table(data, colWidths=[180, 60, 80, 80])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, black),
        ("BACKGROUND", (0, 0), (-1, 0), lightgrey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))


    # Footer
    elements.append(
        Paragraph(
            "Thank you for using Arogyam Health Services.",
            styles["Italic"]
        )
    )


    doc.build(elements)

    return filename




