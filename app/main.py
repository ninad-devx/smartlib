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

app=FastAPI(title="Smartlib Ecosystem")

app.add_middleware(
    SessionMiddleware,secret_key="SMARTLIB_SESSION_SECRET"
)
#template location
templates=Jinja2Templates(directory="app/templates")
#serving the auth routers 
app.include_router(auth_router,prefix="/api/auth",tags=["Authentication"])
#book router
app.include_router(book_router,prefix="/api",tags=["Books"])

#borrow router
app.include_router(
    borrow_router,
    prefix="/api",
    tags=["Borrowing"]
)

#rfid router

app.include_router(
    rfid_router,
    prefix="/api",
    tags=['RFID']
)

#hardware gateway router
app.include_router(
    hardware_router,
    prefix="/api/v1/hardware",
    tags=["Hardware"]
)




@app.get('/')
def home():
    return {'message': 'Smartlib running'}


@app.get("/login")
def login_page(request: Request):
    
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )

@app.get("/student")
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

@app.get("/teacher")
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

@app.get("/librarian")
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

@app.get("/profile")
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
            "rfid_uid":user.rfid_uid,
            "borrow_count": borrow_count,
            "visit_count": visit_count,
            "hours_spent": round(
             minutes_spent / 60,
             1
)
        }
    )

@app.get("/books-page")
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

@app.get("/circulation")
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

@app.get("/search-books")
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

@app.get("/attendance-page")
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

@app.get("/renewals")
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

