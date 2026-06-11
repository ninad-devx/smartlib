from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
import app.services.rfid_state as rfid_state
from app.models.user import User
from app.services.audit_service import log_action

from app.services.rfid_service import link_rfid

router=APIRouter()

@router.post("/rfid/link")
def link_card(
    user_id: int,
    rfid_uid: str,
    db: Session = Depends(get_db)
):
    success, message = link_rfid(
        db,
        user_id,
        rfid_uid
    )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user:
        log_action(
            db,
            f"{user.name} linked RFID",
            user.id
        )

    return {
        "success": success,
        "message": message
    }

@router.post("/rfid/start-link")
def start_link(user_id:int):

    rfid_state.pending_user_id=user_id
    return {
        "success":True,
        "message":"scan RFID CARD NOW"
    }