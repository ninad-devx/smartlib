from app.models.user import User
from app.models.book import Book
from app.models.borrow import Borrowrecord
from app.models.attendance import Attendancelog
from datetime import datetime

def get_librarian_stats(db):
    total_user=db.query(User).count()
    
    total_books=db.query(Book).count()

    active_loans=(
        db.query(Borrowrecord).filter(Borrowrecord.status=="borrowed").count()
    )

    current_visitors=( db.query(Attendancelog).filter(Attendancelog.exit_time==None).count())

    today=datetime.utcnow().date()

    today_attendance=(db.query(Attendancelog).filter(Attendancelog.entry_time>=today).count())

    recent_activity = (
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
    .limit(10)
    .all()
)
    current_visitors = (
    db.query(Attendancelog)
    .filter(
        Attendancelog.exit_time == None
    )
    .count()
)
    

    return {
        "total_users":total_user,
        "total_books":total_books,
        "active_loans":active_loans,
        "current_visitors":current_visitors,
        "today_attendance": today_attendance,
        "recent_activity": recent_activity,
        "current_visitors": current_visitors
    }