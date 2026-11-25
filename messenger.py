import os
import smtplib
import requests
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv(override=True)


def send_email(subject: str, text_body: str, html_body: str) -> str:
    enabled = os.getenv("SEND_EMAIL_ENABLED", "false").lower() == "true"
    recipients = [
        item.strip()
        for item in os.getenv("SALES_RECIPIENTS", "").split(",")
        if item.strip()
    ]

    if not enabled:
        return (
            "DRY RUN: Email sending is disabled. "
            f"Would have sent '{subject}' to {recipients or '[no recipients configured]'}."
        )

    if not recipients:
        raise RuntimeError("SEND_EMAIL_ENABLED is true, but SALES_RECIPIENTS is empty.")

    email_address = os.getenv("EMAIL_ADDRESS", "").strip()
    app_password = os.getenv("EMAIL_APP_PASSWORD", "").strip()
    smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))

    if not email_address or not app_password:
        raise RuntimeError("Configure EMAIL_ADDRESS and EMAIL_APP_PASSWORD.")

    message = EmailMessage()
    message["From"] = email_address
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, app_password)
        server.send_message(message)

    return f"SMTP accepted the message for {len(recipients)} recipient(s)."


def push(message: str) -> dict:
    user = os.getenv("PUSHOVER_USER", "").strip()
    token = os.getenv("PUSHOVER_TOKEN", "").strip()
    if not user or not token:
        raise RuntimeError("Configure PUSHOVER_USER and PUSHOVER_TOKEN.")

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={"user": user, "token": token, "message": message},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
