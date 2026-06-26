from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
from datetime import timedelta

from app.utils.auth import require_login, require_role
from app.core.database import Sessionlocal
from app.services.dashboard_service import get_librarian_stats

from app.models.user import User
from app.models.attendance import Attendancelog
from app.models.borrow import Borrowrecord
from app.models.book import Book
from app.models.renewal import RenewalRequest
from app.services.fine_service import calculate_fine


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")





@router.get("/student")
def student_dashboard(request: Request):
    db = Sessionlocal()

    require_login(request)
    require_role(request, ["student"])

    user_id = request.session["user_id"]
    now = datetime.utcnow()
    # ---------------------------
    # Borrowed books
    # ---------------------------
    borrowed_books = (
        db.query(Borrowrecord, Book)
        .join(Book, Borrowrecord.book_id == Book.id)
        .filter(Borrowrecord.user_id == user_id)
        .order_by(Borrowrecord.id.desc())
        .all()
    )
    borrow_details = []

    for borrow, book in borrowed_books:

     fine = calculate_fine(
        borrow.due_date
    )

     days_remaining = (
        borrow.due_date -
        datetime.utcnow()
    ).days

     borrow_details.append({

        "borrow_id": borrow.id,

        "book_title": book.title,

        "book_image": book.image_url,

        "borrow_date": borrow.borrow_date,

        "due_date": borrow.due_date,

        "status": borrow.status,

        "days_remaining": days_remaining,

        "fine": fine
    })

    # ---------------------------
    # Attendance history
    # ---------------------------
    attendance_history = (
        db.query(Attendancelog)
        .filter(Attendancelog.user_id == user_id)
        .order_by(Attendancelog.id.desc())
        .limit(20)
        .all()
    )

    # ---------------------------
    # Renewals
    # ---------------------------
    renewals = (
        db.query(RenewalRequest)
        .join(Borrowrecord, RenewalRequest.borrow_id == Borrowrecord.id)
        .filter(Borrowrecord.user_id == user_id)
        .all()
    )

    renewal_map = {
        r.borrow_id: r.status
        for r in renewals
    }

    # ---------------------------
    # Renewal allowed check (FIXED)
    # ---------------------------
    renewal_allowed = {}

    for borrow, book in borrowed_books:

      if borrow.status != "borrowed":
         renewal_allowed[borrow.id] = False
         continue

      if not borrow.due_date:
         renewal_allowed[borrow.id] = False
         continue

      days_left = (borrow.due_date - now).days

      renewal_allowed[borrow.id] = (
    0 <= days_left <= 3
)

      
    # ---------------------------
    # Borrowed count
    # ---------------------------
    borrowed_count = sum(
        1 for b, book in borrowed_books
        if b.status == "borrowed"
    )

    # ---------------------------
    # Hours in library
    # ---------------------------
    hours_in_library = 0

    for log in attendance_history:
        if log.entry_time and log.exit_time:
            diff = log.exit_time - log.entry_time
            hours_in_library += diff.total_seconds() / 3600

    hours_in_library = round(hours_in_library, 2)

    # ---------------------------
    # Fine calculation
    # ---------------------------
    pending_fines = 0

    for b, book in borrowed_books:
        if b.status == "borrowed" and b.due_date:
            if b.due_date < now:
                days_late = (now - b.due_date).days
                pending_fines += days_late * 5

    # ---------------------------
    # Render
    # ---------------------------
    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
            "request": request,
            "name": request.session.get("name"),

            "borrow_details": borrow_details,
            "attendance_history": attendance_history,
            "renewals": renewals,
            "renewal_map": renewal_map,

            "borrowed_count": borrowed_count,
            "hours_in_library": hours_in_library,
            "pending_fines": pending_fines,

            "renewal_allowed": renewal_allowed,
            "timedelta": timedelta
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
    borrow_details = []

    for borrow, book in borrowed_books:
        fine = calculate_fine(borrow.due_date)

        days_remaining = 0

        if borrow.due_date:
          days_remaining = (
             borrow.due_date - datetime.utcnow()
             ).days

        borrow_details.append({
         "borrow_id": borrow.id,
         "book_title": book.title,
         "book_image": book.image_url,
         "borrow_date": borrow.borrow_date,
         "due_date": borrow.due_date,
         "status": borrow.status,
         "days_remaining": days_remaining,
         "fine": fine,
    })
    


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
        # ---------------------------
    # Borrowed count
    # ---------------------------
    borrowed_count = sum(
        1 for b, book in borrowed_books
        if b.status == "borrowed"
    )

    # ---------------------------
    # Hours in library
    # ---------------------------
    hours_in_library = 0

    for log in attendance_history:
        if log.entry_time and log.exit_time:
            diff = log.exit_time - log.entry_time
            hours_in_library += diff.total_seconds() / 3600

    hours_in_library = round(hours_in_library, 2)

    # ---------------------------
    # Pending fines
    # ---------------------------
    pending_fines = 0

    now = datetime.utcnow()

    for b, book in borrowed_books:
        if b.status == "borrowed" and b.due_date:
            if b.due_date < now:
                days_late = (now - b.due_date).days
                pending_fines += days_late * 5

    return templates.TemplateResponse(
        request=request,
        name="teacher.html",
        context={
            "request": request,
            "name": request.session.get("name"),
            "borrow_details": borrow_details,
            "attendance_history": attendance_history,
            "borrowed_count": borrowed_count,
            "hours_in_library": hours_in_library,
            "pending_fines": pending_fines,
            "timedelta": timedelta
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
    overdue_details = []

    for borrow, user, book in overdue_records:

        fine = calculate_fine(
           borrow.due_date
    )

        overdue_details.append({

         "borrow_id": borrow.id,

         "student_name": user.name,

         "student_id": user.university_id,

         "book_title": book.title,

         "due_date": borrow.due_date,

         "fine": fine
    })
    


    return templates.TemplateResponse(
    request=request,
    name="librarian.html",
    context={
        "request": request,
        "name": request.session.get("name"),
        "stats": stats,
        "current_inside": current_inside,
        "overdue_records": overdue_records,
        "now":datetime.utcnow(),
        "overdue_details": overdue_details,
        "timedelta": timedelta

        
    }
)
