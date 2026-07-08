import os
from email.message import EmailMessage
import aiosmtplib


async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = os.getenv("MAIL_FROM")
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=os.getenv("MAIL_HOST"),
        port=int(os.getenv("MAIL_PORT", "587")),
        username=os.getenv("MAIL_USERNAME"),
        password=os.getenv("MAIL_PASSWORD"),
        start_tls=True
    )