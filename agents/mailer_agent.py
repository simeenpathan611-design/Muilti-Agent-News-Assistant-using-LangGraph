# Sends the final newsletter to subscribers
# agents/mailer_agent.py

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

DATA_PATH = Path("data/subscribers.json")
NEWSLETTER_PATH = Path("data/cache/newsletter.html")

def send_email(to_email, subject, html_content):
    """Send one HTML email via Gmail SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")
        return False

def run_mailer(subject="Your Daily AI Newsletter"):
    """Send newsletter.html to all subscribers."""
    if not EMAIL_USER or not EMAIL_PASS:
        raise ValueError("Missing EMAIL_USER or EMAIL_PASS in .env")

    if not NEWSLETTER_PATH.exists():
        raise FileNotFoundError("Newsletter HTML not found. Run writer_agent first.")

    # Load newsletter HTML
    html_content = NEWSLETTER_PATH.read_text(encoding="utf-8")

    # Load subscribers
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        subscribers = json.load(f)

    print(f"📧 Sending newsletter to {len(subscribers)} subscribers...")

    success, failed = 0, 0
    for sub in subscribers:
        name = sub.get("name", "Subscriber")
        email = sub.get("email")
        if not email:
            continue

        personalized_html = html_content.replace(
            "Stay tuned for more AI insights!",
            f"Stay tuned for more AI insights, {name}!"
        )

        if send_email(email, subject, personalized_html):
            success += 1
        else:
            failed += 1

    print(f"✅ Sent: {success}, ❌ Failed: {failed}")

# Test run
if __name__ == "__main__":
    run_mailer()
