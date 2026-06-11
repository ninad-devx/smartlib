from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.api.auth import router as auth_router
from app.utils.auth import require_login,require_role
from app.api.books import router as book_router
from app.api.borrow import (router as borrow_router)
from app.core.database import Sessionlocal
from app.services.dashboard_service import get_librarian_stats
from app.api.rfid import( router as rfid_router)
from app.api.hardware import (
    router as hardware_router
)
from app.models.user import User
from app.models.attendance import Attendancelog
from datetime import datetime
from app.models.borrow import Borrowrecord
from app.models.book import Book
from app.models.renewal import RenewalRequest
from sqlalchemy import func
from fastapi import APIRouter

router = APIRouter()
templates = Jinja2Templates(directory="templates")





@router.get("/student")
def student_dashboard(request: Request):
    print(request.session)
    db=Sessionlocal()

    require_login(request)
    require_role(request, ["student"])

    borrowed_books = (
    db.query(
        Borrowrecord,
        Book
    )
    .join(
        Book,
        Borrowrecord.book_id == Book.id
    )
    .filter(
        Borrowrecord.user_id ==
        request.session["user_id"]
    )
    .order_by(
        Borrowrecord.id.desc()
    )
    .all()
)
    attendance_history = (
    db.query(Attendancelog)
    .filter(
        Attendancelog.user_id ==
        request.session["user_id"]
    )
    .order_by(
        Attendancelog.id.desc()
    )
    .limit(20)
    .all()
)
    renewals = (
    db.query(
        RenewalRequest
    )
    .join(
        Borrowrecord,
        RenewalRequest.borrow_id ==
        Borrowrecord.id
    )
    .filter(
        Borrowrecord.user_id ==
        request.session["user_id"]
    )
    .all()
)
    renewal_map = {
    r.borrow_id: r.status
    for r in renewals
}
    
    

    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
            "request": request,
            "name": request.session.get("name"),
            "borrowed_books": borrowed_books,
            "attendance_history": attendance_history,
            "renewals": renewals,
            "renewal_map": renewal_map
        }
    )


@router.get("/teacher")
def teacher_dashboard(request: Request):
    require_login(request)

    require_role(
        request,
        ["teacher"]
    )
    db=Sessionlocal()
    borrowed_books = (
    db.query(
        Borrowrecord,
        Book
    )
    .join(
        Book,
        Borrowrecord.book_id == Book.id
    )
    .filter(
        Borrowrecord.user_id ==
        request.session["user_id"]
    )
    .order_by(
        Borrowrecord.id.desc()
    )
    .all()
)
    attendance_history = (
    db.query(Attendancelog)
    .filter(
        Attendancelog.user_id ==
        request.session["user_id"]
    )
    .order_by(
        Attendancelog.id.desc()
    )
    .limit(20)
    .all()
)

    return templates.TemplateResponse(
    request=request,
    name="teacher.html",
    context={
        "request": request,
        "name": request.session.get("name"),
        "borrowed_books": borrowed_books,
        "attendance_history": attendance_history
    }
)



@router.get("/librarian")
def librarian_dashboard(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    db = Sessionlocal()

    stats = get_librarian_stats(db)
    

    current_inside = (
    db.query(
        Attendancelog,
        User
    )
    .join(
        User,
        Attendancelog.user_id == User.id
    )
    .filter(
        Attendancelog.exit_time == None
    )
    .all()
)
    overdue_records = (
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
    .filter(
        Borrowrecord.due_date < datetime.utcnow()
    )
    .all()
)
    stats["overdue_books"] = len(
    overdue_records
)
    


    return templates.TemplateResponse(
    request=request,
    name="librarian.html",
    context={
        "request": request,
        "name": request.session.get("name"),
        "stats": stats,
        "current_inside": current_inside,
        "overdue_records": overdue_records,
        "now":datetime.utcnow()
        
    }
)
