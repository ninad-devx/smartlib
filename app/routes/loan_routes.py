from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from app.core.database import Sessionlocal

from app.models.borrow import Borrowrecord
from app.models.user import User
from app.models.book import Book

from app.utils.auth import (
    require_login,
    require_role
)

from app.services.fine_service import (
    calculate_fine
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/active-loans")
def active_loans_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    db = Sessionlocal()

    records = (

        db.query(
            Borrowrecord,
            User,
            Book
        )

        .join(
            User,
            Borrowrecord.user_id == User.id
        )

        .join(
            Book,
            Borrowrecord.book_id == Book.id
        )

        .filter(
            Borrowrecord.status == "borrowed"
        )

        .all()
    )

    loan_details = []

    for borrow, user, book in records:

        loan_details.append({

            "borrow_id": borrow.id,

            "student_name": user.name,

            "student_id": user.university_id,

            "book_title": book.title,

            "borrow_date": borrow.borrow_date,

            "due_date": borrow.due_date,

            "fine": calculate_fine(
                borrow.due_date
            ),

            "status": borrow.status
        })

    return templates.TemplateResponse(
        request=request,
        name="active_loans.html",
        context={
            "request": request,
            "loan_details":
            loan_details
        }
    )