from datetime import datetime
from datetime import timedelta

from app.models.book import Book
from app.models.user import User
from app.models.borrow import Borrowrecord


def borrow_book_service(
    db,
    user_id,
    book_id
):

    user = db.get(
        User,
        user_id
    )

    if not user:
        return False, "User not found"

    book = db.get(
        Book,
        book_id
    )

    if not book:
        return False, "Book not found"

    if book.available_quantity <= 0:
        return False, "Book unavailable"

    due_days = 14

    if user.role == "teacher":
        due_days = 30

    borrow = Borrowrecord(
        user_id=user.id,
        book_id=book.id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow()
        + timedelta(days=due_days),
        status="borrowed"
    )

    book.available_quantity -= 1

    db.add(borrow)

    db.commit()

    return True, "Book Borrowed"