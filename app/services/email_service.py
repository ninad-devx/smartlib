import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise ValueError("Missing RESEND_API_KEY")


def send_email(receiver_email, subject, body):

    try:

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": "onboarding@resend.dev",
                "to": [receiver_email],
                "subject": subject,
                "text": body,
            },
        )

        print(response.text)

        return response.status_code in [200, 201]

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

    body = f"""Hello {user_name},

Your book has been issued successfully.

Borrow ID: {borrow_id}
Book: {book_title}
Due Date: {due_date}

Fine Policy:
20 Tk per overdue day.

Thank you for using SmartLib Ecosystem.
"""

    return send_email(
        user_email,
        subject,
        body
    )