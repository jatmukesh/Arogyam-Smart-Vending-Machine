

# utils/pdf_report.py

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black, lightgrey
import os


def generate_bp_pdf(
    filename,
    name,
    age,
    email,
    timestamp,
    systolic,
    diastolic,
    pulse,
    category
):
    """
    Generate Blood Pressure PDF report
    """

    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=40,
                            bottomMargin=40)

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(
        Paragraph("<b>Arogyam Smart Health Kiosk</b>", styles["Title"])
    )
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph("Blood Pressure Report", styles["h2"])
    )
    elements.append(Spacer(1, 20))

    # User info
    info = f"""
    <b>Name:</b> {name}<br/>
    <b>Age:</b> {age}<br/>
    <b>Email:</b> {email}<br/>
    <b>Date & Time:</b> {timestamp}
    """

    elements.append(Paragraph(info, styles["Normal"]))
    elements.append(Spacer(1, 25))

    # Table Data
    table_data = [
        ["Parameter", "Value"],
        ["Systolic (mmHg)", str(systolic)],
        ["Diastolic (mmHg)", str(diastolic)],
        ["Pulse (BPM)", str(pulse)],
        ["Category", category],
    ]

    table = Table(table_data, colWidths=[200, 200])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, black),
        ("BACKGROUND", (0, 0), (-1, 0), lightgrey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    # Footer
    elements.append(
        Paragraph(
            "This report is generated automatically by Arogyam Health System.",
            styles["Italic"]
        )
    )

    doc.build(elements)

    return filename

