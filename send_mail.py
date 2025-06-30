
import smtplib
from email.message import EmailMessage
import config
import os

def send_certificate(email_to, name, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your Internship Certificate'
    msg['From'] = config.MAIL_USERNAME
    msg['To'] = email_to

    msg.set_content(f"Hi {name},\n\nAttached is your internship certificate.\n\nRegards,\nTeam")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    try:
        with smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT) as server:
            server.starttls()
            server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email Error:", e)
        return False
