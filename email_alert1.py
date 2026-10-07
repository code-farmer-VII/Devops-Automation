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


def send_alert(
    repository,
    workflow,
    status,
    url,
):

    email = EmailMessage()

    email["Subject"] = (
        f"🚨 GitHub CI/CD Failure - {repository}"
    )

    email["From"] = EMAIL_FROM
    email["To"] = EMAIL_TO

    body = f"""
GitHub Repository Incident Detected

Repository:
{repository}

Workflow:
{workflow}

Status:
{status}

Details:
Your GitHub CI/CD workflow has failed.

View GitHub Actions:
{url}

--------------------------------
GitHub Repository Monitor
"""

    email.set_content(body)

    try:

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=20
        ) as server:

            server.starttls()

            server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            server.send_message(email)

        print("📧 Alert email sent successfully.")

    except Exception as e:

        print(f"❌ Email failed: {e}")