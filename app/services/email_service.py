import os
import smtplib
import traceback

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

MAIL_EMAIL = os.getenv("MAIL_EMAIL")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


# ----------------------------
# SAFE VALIDATION (IMPORTANT)
# ----------------------------
if not MAIL_EMAIL or not MAIL_PASSWORD:
    raise ValueError("Missing MAIL_EMAIL or MAIL_PASSWORD in environment variables")


def send_email(receiver_email, subject, body):
    server = None

    try:
        message = MIMEMultipart()
        message["From"] = MAIL_EMAIL
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain", "utf-8"))

        # ----------------------------
        # SMTP SSL CONNECTION (GMAIL)
        # ----------------------------
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)

        server.login(MAIL_EMAIL, MAIL_PASSWORD)

        server.sendmail(
            MAIL_EMAIL,
            receiver_email,
            message.as_string()
        )

        return True

    except Exception:
        traceback.print_exc()
        return False

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


# ----------------------------
# BORROW RECEIPT EMAIL
# ----------------------------
def send_borrow_receipt(
    user_email,
    user_name,
    book_title,
    borrow_id,
    due_date
):

    subject = "SmartLib Borrow Receipt"

    body = f"""Hello {user_name},

Your book has been issued successfully.

Borrow ID: {borrow_id}
Book: {book_title}
Due Date: {due_date}

Fine Policy:
20 Tk per overdue day.

Thank you for using SmartLib Ecosystem.
"""

    return send_email(user_email, subject, body)