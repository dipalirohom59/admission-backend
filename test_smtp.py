import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

smtp_server = "smtp.gmail.com"
port = 465
sender_email = os.getenv("MAIL_USERNAME")
password = os.getenv("MAIL_PASSWORD")

message = """\
Subject: Test Email

This is a test email sent from Python."""

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, message)
    print("Test email sent successfully!")
except Exception as e:
    print(f"An error occurred: {e}")