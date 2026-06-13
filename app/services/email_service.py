import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

import os

load_dotenv()


MAIL_EMAIL = os.getenv("MAIL_EMAIL")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


def send_email(
    receiver_email,
    subject,
    body
):

    try:

        message = MIMEMultipart()

        message["From"] = MAIL_EMAIL
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            MAIL_EMAIL,
            MAIL_PASSWORD
        )

        server.sendmail(
            MAIL_EMAIL,
            receiver_email,
            message.as_string()
        )

        server.quit()

        return True

    except Exception as e:

        print("EMAIL ERROR:", e)

        return False
    

def send_borrow_receipt(
    user_email,
    user_name,
    book_title,
    borrow_id,
    due_date
):

    subject = "SmartLib Borrow Receipt"

    body = f"""
Hello {user_name},

Your book has been issued successfully.

Borrow ID: {borrow_id}

Book: {book_title}

Due Date:
{due_date}

Fine Policy:
20 Tk per overdue day.

Thank you for using SmartLib Ecosystem.
"""

    send_email(
        user_email,
        subject,
        body
    )

    