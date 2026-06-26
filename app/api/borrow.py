from datetime import datetime
from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.book import Book
from app.models.borrow import Borrowrecord
from app.schemas.borrow import(Borrowcreate,Returnbook)
from app.models.renewal import RenewalRequest
from app.schemas.renewal import RenewalRequestCreate
from app.schemas.renewal import (
    RenewalRequestCreate,
    RenewalApprove
)
from app.services.audit_service import log_action
from app.services.email_service import send_borrow_receipt

router=APIRouter()



@router.post("/borrow")
def borrow_book(
    payload: Borrowcreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.university_id ==
            payload.university_id
        )
        .first()
    )

    if not user:
        return {
            "success": False,
            "message": "student not found"
        }

    book = (
        db.query(Book)
        .filter(
            Book.id == payload.book_id
        )
        .first()
    )

    if not book:
        return {
            "success": False,
            "message": "book not found"
        }

    if book.available_quantity <= 0:
        return {
            "success": False,
            "message": "book not available"
        }

    due_date = (
        datetime.utcnow()
        + timedelta(
            days=payload.borrow_days
        )
    )

    record = Borrowrecord(
        user_id=user.id,
        book_id=payload.book_id,
        borrow_date=datetime.utcnow(),
        due_date=due_date,
        status="borrowed"
    )

    book.available_quantity -= 1
    

    db.add(record)
    db.commit()
    db.refresh(record)
    log_action(
        db,
        f"{user.name} borrowed book {book.title}",
        user.id
)

    try:
       email_sent = send_borrow_receipt(
        user.email,
        user.name,
        book.title,
        record.id,
        due_date
      )

       if not email_sent:
         log_action(
            db,
            f"EMAIL FAILED for borrow {record.id} - {user.email}",
            user.id
        )

    except Exception as e:
      log_action(
        db,
        f"EMAIL ERROR for borrow {record.id}: {str(e)}",
        user.id
    )

    return {
    "success": True,
    "message": f"{user.name} borrowed '{book.title}'",
    "borrow_id": record.id,
    "student_name": user.name,
    "student_id": user.university_id,
    "book_title": book.title,
    "borrow_date": record.borrow_date,
    "due_date": record.due_date
}




@router.post("/return")
def return_book(payload:Returnbook,db:Session=Depends(get_db)):

    borrow=db.query(Borrowrecord).get(
        payload.borrow_id
    )

    if not borrow:
        return {
            "success":False,
            "message":"borrow record not found"
        }
    
    if borrow.status=="returned":
        return {
            "success":False,
            "message":"already returned"
        }
    

    book=db.query(Book).get(borrow.book_id)
    book.available_quantity+=1
    borrow.return_date=datetime.utcnow()
    borrow.status="returned"
    
    db.commit()
    user = db.get(
    User,
    borrow.user_id
)

    log_action(
     db,
     f"{user.name} returned book {book.title}",
     user.id
)
    

    return {
    "success": True,
    "message": f"{user.name} returned the book {book.title}"
}

@router.get("/borrow/history/{user_id}")
def borrow_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    records = (
        db.query(Borrowrecord)
        .filter(
            Borrowrecord.user_id == user_id
        )
        .all()
    )

    result = []

    for r in records:
      book = db.get(Book, r.book_id)

      result.append({
        "borrow_id": r.id,
        "book_title": book.title if book else None,
        "book_image": book.image if book else None,
        "borrow_date": r.borrow_date,
        "due_date": r.due_date,
        "status": r.status
    })

    return result


@router.get("/borrow/active")
def active_loans(
    db: Session = Depends(get_db)
):

    records = (
        db.query(Borrowrecord)
        .filter(
            Borrowrecord.status == "borrowed"
        )
        .all()
    )

    return records


@router.post("/renew-request")
def create_renewal_request(
    payload: RenewalRequestCreate,
    db: Session = Depends(get_db)
):
    borrow = db.get(Borrowrecord, payload.borrow_id)

    if not borrow:
        return {
            "success": False,
            "message": "Borrow record not found"
        }

    request = RenewalRequest(

    borrow_id=
    payload.borrow_id,

    request_date=
    datetime.utcnow(),

    requested_days=
    payload.requested_days,

    status="pending"

)

    db.add(request)
    db.commit()
    user = db.get(User, borrow.user_id)

    log_action(
        db,
        f"{user.name} requested renewal for borrow #{borrow.id}",
        user.id
    )

    return {
        "success": True,
        "message": "Renewal Requested"
    }

@router.post("/renew-approve")
def approve_renewal(
    payload: RenewalApprove,
    db: Session = Depends(get_db)
):

    renewal = db.query(RenewalRequest).get(payload.renewal_id)

    if not renewal:
        return {
            "success": False,
            "message": "Renewal request not found"
        }

    if renewal.status != "pending":
        return {
            "success": False,
            "message": f"Renewal already {renewal.status}"
        }

    borrow = db.query(Borrowrecord).get(renewal.borrow_id)

    if not borrow:
        return {
            "success": False,
            "message": "Borrow record not found"
        }

    if borrow.status != "borrowed":
        return {
            "success": False,
            "message": "Cannot renew returned book"
        }

    # ----------------------------
    # UPDATE DUE DATE
    # ----------------------------
    borrow.due_date = borrow.due_date + timedelta(
        days=renewal.requested_days
    )

    renewal.status = "approved"

    db.commit()
    user = db.get(User, borrow.user_id)

    log_action(
        db,
        f"{user.name}'s renewal approved for borrow #{borrow.id}",
        user.id
    )

    return {
        "success": True,
        "message": "Renewal approved",
        "borrow_id": borrow.id,
        "new_due_date": borrow.due_date
    }