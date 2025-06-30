from fpdf import FPDF
import os

def generate_certificate(logo_path, name, course, start_date, end_date):
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_margins(10, 10, 10)

    pdf.image('static/bg.png', 0, 0, 300)  # Optional background

    # Uncomment to show logo:
    # pdf.image(logo_path, 80, 15, 150)

    pdf.set_y(45)
    pdf.set_font("Helvetica", "B", 45)
    pdf.set_text_color(0, 120, 160)
    pdf.cell(0, 15, "CERTIFICATE", ln=True, align="C")
    pdf.set_font("Helvetica", "BI", 18)
    pdf.cell(0, 15, "OF INTERNSHIP", ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 15)
    pdf.ln(5)
    pdf.cell(0, 10, 'This is to certify that', ln=True, align='C')

    pdf.set_font("Helvetica", "B", 30)
    pdf.cell(0, 15, name, ln=True, align='C')

    pdf.set_font("Helvetica", "", 15)
    pdf.cell(0, 10, 'has successfully completed the internship in', ln=True, align='C')
    pdf.set_font("Helvetica", "I", 15)
    pdf.cell(0, 10, course, ln=True, align='C')
    pdf.cell(0, 10, f'from {start_date} to {end_date}', ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 10, 'We wish you good luck in all your future endeavors.', ln=True, align='C')

    filepath = f"static/certificates/{name.replace(' ', '_')}_certificate.pdf"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pdf.output(filepath)
    return filepath
