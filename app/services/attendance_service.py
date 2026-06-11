from datetime import datetime, timedelta

from app.models.user import User
from app.models.attendance import Attendancelog


def process_rfid_scan(db, rfid_uid):

    user = (
        db.query(User)
        .filter(User.rfid_uid == rfid_uid)
        .first()
    )

    if not user:
        return {
            "header": "DENIED",
            "line1": "Unknown Card",
            "line2": "",
            "footer": "",
            "buzzer_ms": 1000
        }

    # -------------------------------
    # 🔒 NEW: debounce / anti double-scan logic
    # -------------------------------
    latest_record = (
        db.query(Attendancelog)
        .filter(Attendancelog.user_id == user.id)
        .order_by(Attendancelog.id.desc())
        .first()
    )

    if latest_record:
        last_time = latest_record.exit_time or latest_record.entry_time

        if last_time and (datetime.utcnow() - last_time) < timedelta(seconds=5):
            return {
                "header": "WAIT",
                "line1": "Please Wait",
                "line2": "",
                "footer": "",
                "buzzer_ms": 100
            }

    # -------------------------------
    # ENTRY / EXIT logic
    # -------------------------------
    open_session = (
        db.query(Attendancelog)
        .filter(
            Attendancelog.user_id == user.id,
            Attendancelog.exit_time == None
        )
        .first()
    )

    if not open_session:
        attendance = Attendancelog(
            user_id=user.id,
            entry_time=datetime.utcnow()
        )
        db.add(attendance)
        db.commit()

        return {
            "header": "ENTRY",
            "line1": "Welcome",
            "line2": user.name,
            "footer": "Library Entry",
            "buzzer_ms": 200
        }

    duration = int(
        (datetime.utcnow() - open_session.entry_time)
        .total_seconds() / 60
    )

    open_session.exit_time = datetime.utcnow()
    open_session.duration_minutes = duration

    db.commit()

    return {
        "header": "EXIT",
        "line1": "Goodbye",
        "line2": user.name,
        "footer": f"{duration} mins",
        "buzzer_ms": 400
    }