import smtplib
from email.message import EmailMessage

from config import (
    EMAIL_FROM,
    EMAIL_TO,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
)


def send_alert(subject: str, body: str):
    """
    Unified email alert sender for all monitors.
    """
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = EMAIL_FROM
    email["To"] = EMAIL_TO

    email.set_content(body)

    try:
        # Using timeout to prevent hanging if network is blocked
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(email)

        print(f"📧 Alert email sent successfully: {subject}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
