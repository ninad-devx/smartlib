from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_

from app.utils.auth import require_login, require_role
from app.core.database import Sessionlocal

from app.models.user import User
from app.models.attendance import Attendancelog
from app.models.borrow import Borrowrecord
from app.models.book import Book
from app.models.renewal import RenewalRequest


from sqlalchemy import func

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get('/')
def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )



@router.get("/login")
def login_page(request: Request):
    
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )


@router.get("/profile")
def profile_page(
    request: Request
):

    require_login(request)
    db=Sessionlocal()

    user=db.get(User,request.session.get("user_id"))
    borrow_count = (
    db.query(Borrowrecord)
    .filter(
        Borrowrecord.user_id ==
        user.id
    )
    .count()
)
    visit_count = (
    db.query(Attendancelog)
    .filter(
        Attendancelog.user_id ==
        user.id
    )
    .count()
)
    minutes_spent = (
    db.query(
        func.sum(
            Attendancelog.duration_minutes
        )
    )
    .filter(
        Attendancelog.user_id ==
        user.id
    )
    .scalar()
)

    if not minutes_spent:
     minutes_spent = 0
    



    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            
            "request": request,
            "user_id": request.session.get("user_id"),
            "name": request.session.get("name"),
            "role": request.session.get("role"),
            "email":user.email,
            "university_id":user.university_id,
            "rfid_uid":user.rfid_uid,
            "borrow_count": borrow_count,
            "visit_count": visit_count,
            "hours_spent": round(
             minutes_spent / 60,
             1
)
        }
    )


@router.get("/books-page")
def books_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    return templates.TemplateResponse(
        request=request,
        name="books.html",
        context={
            "request": request
        }
    )


@router.get("/circulation")
def circulation_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    return templates.TemplateResponse(
        request=request,
        name="circulation.html",
        context={
            "request": request
        }
    )


@router.get("/search-books")
def search_books_page(
    request: Request
):

    require_login(request)

    return templates.TemplateResponse(
        request=request,
        name="search_books.html",
        context={
            "request": request
        }
    )


@router.get("/attendance-page")
def attendance_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )
    db=Sessionlocal()

    records = (
        db.query(
            Attendancelog,
            User
        )
        .join(
            User,
            Attendancelog.user_id == User.id
        )
        .order_by(
            Attendancelog.id.desc()
        )
        .limit(200)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="attendance.html",
        context={
            "request": request,
            "records": records
        }
    )


@router.get("/renewals")
def renewals_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )
    db=Sessionlocal()

    requests_list = (
        db.query(
            RenewalRequest,
            Borrowrecord,
            User,
            Book
        )
        .join(
            Borrowrecord,
            RenewalRequest.borrow_id ==
            Borrowrecord.id
        )
        .join(
            User,
            Borrowrecord.user_id ==
            User.id
        )
        .join(
            Book,
            Borrowrecord.book_id ==
            Book.id
        )
        .filter(
            RenewalRequest.status ==
            "pending"
        )
        .all()
    )
   

    return templates.TemplateResponse(
        request=request,
        name="renewals.html",
        context={
            "request": request,
            "requests_list":
            requests_list
        }
    )


@router.get("/student_search")
def student_page(
    request: Request,
    q: str = ""
):
    require_login(request)

    db = Sessionlocal()

    students = []
    borrows = []
    attendance = []

    if q:
        students = (
    db.query(User)
    .filter(
        or_(
            User.name.ilike(f"%{q}%"),
            User.university_id == int(q) if q.isdigit() else False
        )
    )
    .all()
)

        if len(students) == 1:
            student = students[0]

            borrows = (
                db.query(Borrowrecord)
                .filter(Borrowrecord.user_id == student.id)
                .all()
            )

            attendance = (
                db.query(Attendancelog)
                .filter(Attendancelog.user_id == student.id)
                .all()
            )

    return templates.TemplateResponse(
        request=request,
        name="student_details.html",
        context={
            "request": request,
            "students": students,
            "q": q,
            "borrows": borrows,
            "attendance": attendance
        }
    )