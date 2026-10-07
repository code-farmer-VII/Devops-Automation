import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

LOG_GROUPS = [
    os.getenv("LOG_GROUP_1"),
    os.getenv("LOG_GROUP_2"),
    os.getenv("LOG_GROUP_3"),
]

LOG_GROUPS = [group for group in LOG_GROUPS if group]

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")