from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import Header

from app.core.database import Sessionlocal
from app.services.attendance_service import process_rfid_scan

import app.services.rfid_state as rfid_state

from app.models.user import User

router = APIRouter()


class Hardwarepayload(BaseModel):
    device_id: str
    rfid_uid: str | None = None
    key_pressed: str | None = None


@router.post("/gateway")
def gateway(
    payload: Hardwarepayload,
    x_device_secret: str = Header(None)
):

    if x_device_secret != "SMUCT_SECRET_KEYPAD_DEVICE_1924":
        return {
            "header": "ACCESS DENIED",
            "line1": "Invalid Device",
            "line2": "",
            "footer": "",
            "buzzer_ms": 1000
        }

    db = Sessionlocal()

    if payload.rfid_uid:

        # --------------------------------
        # RFID REGISTRATION MODE
        # --------------------------------
        print("Pending user:", rfid_state.pending_user_id)
        if rfid_state.pending_user_id is not None:

            user = db.get(
                User,
                rfid_state.pending_user_id
            )

            user.rfid_uid = payload.rfid_uid

            db.commit()

            rfid_state.pending_user_id = None

            return {
                "header": "RFID LINKED",
                "line1": user.name,
                "line2": "Card Saved",
                "footer": "",
                "buzzer_ms": 500
            }

        # --------------------------------
        # NORMAL RFID ATTENDANCE MODE
        # --------------------------------
        print("Attendance mode")
        return process_rfid_scan(
            db,
            payload.rfid_uid
        )

    return {
        "header": "SMARTLIB",
        "line1": "Ready",
        "line2": "",
        "footer": "",
        "buzzer_ms": 100
    }